import numpy as np
import sklearn.cross_decomposition as skl_pls

from Orange.data import Table, Domain, Variable, \
    ContinuousVariable, StringVariable
from Orange.data.util import get_unique_names, SharedComputeValue
from Orange.preprocess.score import LearnerScorer
from Orange.regression import SklLearner, SklModel


class _FeatureScorerMixin(LearnerScorer):
    feature_type = Variable
    class_type = ContinuousVariable

    def score(self, data):
        model = self(data)
        return np.abs(model.coefficients), model.domain.attributes


class _PLSCommonTransform:

    def __init__(self, pls_model):
        self.pls_model = pls_model

    def _transform_with_numpy_output(self, X, Y):
        pls = self.pls_model.skl_model
        """
        # the next command does the following
        x_center = X - pls._x_mean
        y_center = Y - pls._y_mean
        t = x_center @ pls.x_rotations_
        u = y_center @ pls.y_rotations_
        """
        t, u = pls.transform(X, Y)
        return np.hstack((t, u))

    def __call__(self, data):
        if data.domain != self.pls_model.domain:
            data = data.transform(self.pls_model.domain)
        if len(data.Y.shape) == 1:
            Y = data.Y.reshape(-1, 1)
        else:
            Y = data.Y
        return self._transform_with_numpy_output(data.X, Y)


class PLSProjector(SharedComputeValue):
    def __init__(self, transform, feature):
        super().__init__(transform)
        self.feature = feature

    def compute(self, _, space):
        return space[:, self.feature]


class PLSModel(SklModel):
    var_prefix_X = "PLS T"
    var_prefix_Y = "PLS U"

    @property
    def coefficients(self):
        coef = self.skl_model.coef_
        return coef

    def predict(self, X):
        vals = self.skl_model.predict(X)
        if len(self.domain.class_vars) == 1:
            vals = vals.ravel()
        return vals

    def __str__(self):
        return 'PLSModel {}'.format(self.skl_model)

    def _get_var_names(self, n, prefix):
        names = [f"{prefix}{postfix}" for postfix in range(1, n + 1)]
        return get_unique_names([var.name for var in self.domain.metas], names)

    def project(self, data):
        if not isinstance(data, Table):
            raise RuntimeError("PLSModel can only project tables")

        transformer = _PLSCommonTransform(self)

        def trvar(i, name):
            return ContinuousVariable(name, compute_value=PLSProjector(transformer, i))

        n_components = self.skl_model.x_loadings_.shape[1]

        var_names_X = self._get_var_names(n_components, self.var_prefix_X)
        var_names_Y = self._get_var_names(n_components, self.var_prefix_Y)

        domain = Domain(
            [trvar(i, var_names_X[i]) for i in range(n_components)],
            data.domain.class_vars,
            list(data.domain.metas) +
            [trvar(n_components + i, var_names_Y[i]) for i in range(n_components)]
        )

        return data.transform(domain)

    def components(self):
        orig_domain = self.domain
        names = [a.name for a in orig_domain.attributes + orig_domain.class_vars]
        meta_name = get_unique_names(names, 'components')

        n_components = self.skl_model.x_loadings_.shape[1]

        meta_vars = [StringVariable(name=meta_name)]
        metas = np.array(
            [[f"Component {i + 1}" for i in range(n_components)]], dtype=object
        ).T
        dom = Domain(
            [ContinuousVariable(a.name) for a in orig_domain.attributes],
            [ContinuousVariable(a.name) for a in orig_domain.class_vars],
            metas=meta_vars)
        components = Table(dom,
                           self.skl_model.x_loadings_.T,
                           Y=self.skl_model.y_loadings_.T,
                           metas=metas)
        components.name = 'components'
        return components

    def coefficients_table(self):
        coeffs = self.coefficients.T
        domain = Domain(
            [ContinuousVariable(f"coef {i}") for i in range(coeffs.shape[1])],
            metas=[StringVariable("name")]
        )
        waves = [[attr.name] for attr in self.domain.attributes]
        coef_table = Table.from_numpy(domain, X=coeffs, metas=waves)
        coef_table.name = "coefficients"
        return coef_table


class PLSRegressionLearner(SklLearner, _FeatureScorerMixin):
    __wraps__ = skl_pls.PLSRegression
    __returns__ = PLSModel
    supports_multiclass = True
    preprocessors = SklLearner.preprocessors

    def fit(self, X, Y, W=None):
        params = self.params.copy()
        params["n_components"] = min(X.shape[1] - 1,
                                     X.shape[0] - 1,
                                     params["n_components"])
        clf = self.__wraps__(**params)
        return self.__returns__(clf.fit(X, Y))

    def __init__(self, n_components=2, scale=True,
                 max_iter=500, preprocessors=None):
        super().__init__(preprocessors=preprocessors)
        self.params = vars()

    def incompatibility_reason(self, domain):
        reason = None
        if not domain.class_vars:
            reason = "Numeric targets expected."
        else:
            for cv in domain.class_vars:
                if not cv.is_continuous:
                    reason = "Only numeric target variables expected."
        return reason

if __name__ == '__main__':
    import Orange

    data = Orange.data.Table('housing')
    learners = [PLSRegressionLearner(n_components=2, max_iter=100)]
    res = Orange.evaluation.CrossValidation()(data, learners)
    for l, ca in zip(learners, Orange.evaluation.RMSE(res)):
        print("learner: {}\nRMSE: {}\n".format(l, ca))
