from scipy.sparse import identity
from scipy.sparse import diags
from scipy.sparse.linalg import spsolve

import numpy
from mpmath import log
from printd import printd
import pandas

from preprocessing import scale_data
from preprocessing import centered_sample_covariance_matrix


# Gaussian Mechanism functions
def gaussian_mechanism(x, scale):
    if any([isinstance(x, float), isinstance(x, int)]):
        M = x + numpy.random.normal(loc=0, scale=scale)
    else:
        M = x + numpy.random.normal(loc=0, scale=scale, size=len(x))
    return M


# Establish parameters: gaussian_sensitivity, MVG_sensitivity
def centered_covariance_query_sensitivity(n, m, c):
    '''
       'A Differential Privacy Mechanism Design Under Matrix-Valued Query'
        Chanyaswad, Dytso, Poor & Mittal 2018, p.18.:
        https://arxiv.org/abs/1802.10077 (accessed 16/12/2018)

       Requires
           n   - divisor of query function
           m   - number of unit values / observations to be varied
                 under adjacency definition
           c   - maximum possible value in range of single observation

       Returns - Sensitivity calculation for zero mean
                 covariance estimation query
                 ie f(X) = n^-1 * transpose(X)X
    '''
    return (2 * float(m) * float(c)**2) / float(n)


def gaussian_mechanism_matrix_sample(data,
                                     epsilon,
                                     delta,
                                     sensitivity,
                                     symmetric=False,
                                     scale_sample=True,
                                     verbose=False):

    n, m = data.shape
    values = data.values

    if symmetric:
        adjusted_epsilon = 2 * epsilon / (pow(n, 2) + n)
        adjusted_delta = 2 * delta / (pow(n, 2) + n)
    else:
        adjusted_epsilon = epsilon / pow(n, 2)
        adjusted_delta = delta / pow(n, 2)

    gaussian_mechanism_scale = (
        pow(2*log(1.25/adjusted_delta), 0.5)*sensitivity
    ) / adjusted_epsilon

    if verbose:
        print('\nAdding Guassian N(0,{std}) \
              noise to matrix shape {s}'.format(
            s=data.shape,
            std=round(gaussian_mechanism_scale, 4))
        )
        print('with differential privacy parameters')
        print('total epsilon\t{te}\nepsilon\t\t{e}\n\
               delta\t\t{d}\nsensitivity\t{s}\n'.format(
            te=epsilon,
            e=adjusted_epsilon,
            d=round(adjusted_delta, 6),
            s=sensitivity)
        )

    if all([symmetric, n == m]):
        sample = numpy.zeros(data.shape)

        for x, y in zip(*numpy.triu_indices(n)):
            sample[x, y] = \
                gaussian_mechanism(values[x, y],
                                   gaussian_mechanism_scale)
            if not(x == y):
                sample[y, x] = sample[x, y]
    else:
        sample = numpy.array([
            numpy.array([
                gaussian_mechanism(v, gaussian_mechanism_scale)
                for v in x
            ])
            for x in values
        ])

    if scale_sample and not(symmetric):
        # rescale to match scaled data set
        sample_bounds = dict()
        for key in data.columns.values:
            sample_bounds[key] = (data[key].min(), data[key].max())

        result = scale_data(pandas.DataFrame(sample,
                                             columns=data.columns.values),
                            target_bounds=sample_bounds,
                            data_bounds=None)
    else:
        result = sample

    return result


def matrixvariate_gaussian_mechanism_sample(data,
                                            epsilon,
                                            delta,
                                            sensitivity,
                                            gamma,
                                            precision_allocation,
                                            precision_direction,
                                            covariance_direction,
                                            covariance_method,
                                            scale_sample=True):

    mvg_mechanism = MVGMechanism(
        epsilon=epsilon,
        delta=delta,
        query_sensitivity=sensitivity,
        query_sup=gamma,
        covariance_direction=covariance_direction,
        sample_shape=data.shape)

    # Set covariance matricies for MVG mechanism
    mvg_mechanism.set_covariance(method=covariance_method,
                                 precision_allocation=precision_allocation,
                                 precision_direction=precision_direction)

    # Generate Differentially Private Sample of data
    sample = mvg_mechanism.generate_sample(data)

    if scale_sample:
        # rescale to match scaled data set
        sample_bounds = dict()
        for key in data.columns.values:
            sample_bounds[key] = (data[key].min(), data[key].max())

        result = scale_data(
            pandas.DataFrame(sample,
                             columns=data.columns.values),
            target_bounds=sample_bounds,
            data_bounds=None)
    else:
        result = sample

    return result


def generalised_harmonic_sum(order, power=1):
    '''
        Naive implementation of generalised harmonic sum
        - vulnerable to floating point errors; and
        - computationally inefficient for large n
    '''
    return numpy.sum([pow(k, -power) for k in range(1, order+1)])


class MVGMechanism(object):
    '''
        mvg_mechanism (Matrix-valued Guassian Mechanism)

        Implementation of the mechanism described in
        'A Differential Privacy Mechanism Design Under Matrix-Valued Query'
        Chanyaswad, Dytso, Poor & Mittal 2018:
        https://arxiv.org/abs/1802.10077 (accessed 16/12/2018)

        Notes:
        MVG can improve utility via directional noise compared to i.i.d noise.
        Two algorithms for implementing directional noise:

            unimodal features / observations
                      - Assumes correlation of features / observations.
                        Suitable for identity query functions ie f(X) = X
            equimodal
                      - Assumes equal correlation of features and observations.
                        Suitable for symmetric query functions ie f(X) = X^T*X
    '''

    def __init__(self,
                 epsilon,
                 delta,
                 query_sensitivity,
                 query_sup,
                 covariance_direction,
                 sample_shape
                 ):
        if self.are_inputs_valid(epsilon,
                                 delta,
                                 query_sensitivity,
                                 query_sup,
                                 covariance_direction,
                                 sample_shape):

            self.epsilon = epsilon
            self.delta = delta
            self.sensitivity = query_sensitivity
            self.query_sup = query_sup
            self.covariance_direction = covariance_direction
            self.shape = sample_shape
            self.set_precision_parameters()
            self.set_precision_budget()

    def set_precision_budget(self):
        n, m = self.shape
        if self.covariance_direction == 'unimodal features':
            ''' Precision budget defined in Theorm 5 p23.
                Derived from equation 23
            '''
            self.precision_budget = (
                pow(-self.precision_parameters['beta'] +
                    pow(pow(self.precision_parameters['beta'], 2) +
                        8 * self.precision_parameters['alpha']
                        * self.epsilon, 0.5), 4) /
                (m * 16 * pow(self.precision_parameters['alpha'], 4))
            )

        elif self.covariance_direction == 'unimodal observations':
            self.precision_budget = None

        elif self.covariance_direction == 'equimodal':
            self.precision_budget = None
        else:
            printd('MVG Mechanism init: set_precision: \
                    supplied covariance_direction {noise} is not valid\n \
                    covariance_direction set to None',
                   noise=self.covariance_direction, level=0)
            self.covariance_direction = None
            self.precision_budget = None

    def set_precision_parameters(self):
        r = numpy.min(self.shape)
        m, n = self.shape
        zeta = float(
            (2*numpy.sqrt(-m*n*log(self.delta))) -
            (2*log(self.delta)) + (m*n)
        )
        printd('r: {r}\nm: {m}\nn: {n}\nzeta: {z}',
               level=6, r=r, m=m, n=n, z=zeta)

        self.precision_parameters = dict()
        ''' Alpha as defined in Theorm 2. p8. equation 1
        '''
        self.precision_parameters['alpha'] = (
            (generalised_harmonic_sum(r)+generalised_harmonic_sum(r, 0.5)
             )*pow(self.query_sup, 2) +
            2*generalised_harmonic_sum(r)*self.query_sup*self.sensitivity
        )
        ''' Beta as defined in Theorm 2. p8. equation 1
        '''
        self.precision_parameters['beta'] = (
            2*pow(n*m, 0.25)*zeta*generalised_harmonic_sum(r)*self.sensitivity
        )
        ''' Omega as defined in Theorm 3. p12. equation 8
        '''
        self.precision_parameters['omega'] = (
            4*generalised_harmonic_sum(r)*self.query_sup*self.sensitivity
        )

    def set_covariance(self,
                       method,
                       precision_direction,
                       precision_allocation,
                       data_covariance=None):

        n, m = self.shape
        self.covariance = dict()

        if method is None or method.lower() == 'pnr':
            print('max-pnr allocation strategy selected')
            print('Warning: max-pnr allocation strategy not yet implemented.')

            # K_f = data_covariance
            #
            # Q_f, K_f_sv, Q_ft = numpy.linalg.svd(
            #     numpy.kron(numpy.transpose(K_f), K_f),
            #     full_matrices=True)
            #
            # a = self.precision_parameters['alpha']
            # b = self.precision_parameters['beta']
            # n, m = self.shape
            #
            # ''' d as defined at the top of p28.
            # '''
            # d = (pow(-b + pow(pow(b, 2) + 8*a*self.epsilon, 0.5), 2) /
            #      (4*pow(a, 2)))
            # ''' c as defined in Theorm 7. p27. equation 25
            # '''
            # c = (d + numpy.sum(pow(K_f_sv, -1))) / (m*n)
            #
            # ''' Derivation from Theorm 7. p27. equation 26
            # '''
            # D_z = [c]*len(K_f_sv) - pow(K_f_sv, -1)
            # D = numpy.diag(pow(D_z, -1))
            #
            # cov_kron = numpy.matmul(numpy.matmul(Q_ft, D), Q_f)

        elif method.lower() == 'binary':
            # record precision direction and allocation
            self.precision_direction = precision_direction
            self.precision_allocation = precision_allocation

            # Covariance matrix singular values
            self.precision = pow(
                numpy.multiply(self.precision_budget,
                               precision_allocation), -0.5)

            # Covariance calculation W*D*W^T
            self.covariance['cov'] = numpy.matmul(
                numpy.matmul(precision_direction,
                             numpy.diag(self.precision)
                             ),
                numpy.transpose(precision_direction))

        else:
            printd('set_covariance: Method {m} is not valid', m=method)
            printd('\tValid methods are: {v}', v=['pnr', 'binary'].join(''))

        # self.covariance['cov'] = cov
        self.covariance['decomposition'] = numpy.matmul(
            precision_direction,
            numpy.diag(pow(self.precision, 0.5)))

    def are_inputs_valid(self,
                         epsilon,
                         delta,
                         query_sensitivity,
                         query_sup,
                         covariance_direction,
                         sample_shape):
        valid = True
        if not(
            isinstance(epsilon, float)
            or isinstance(delta, float)
            or isinstance(query_sensitivity, (int, float, long))
            or isinstance(query_sup, (int, float, long))
        ):
            printd('mvg_mechanism invalid input: incorrect type input\n\
                epsilon is {eptype} should be {eptruth}\n\
                delta is {deltype} should be {deltruth}\n\
                query_sensitivity is {sentype} should be {sentruth}\n\
                query_sup is {suptype} should be {suptruth}\n',
                   eptype=type(), eptruth=float,
                   deltype=type(), deltruth=float,
                   sentype=type(), sentruth=(int, float, long),
                   suptype=type(), suptruth=(int, float, long))
        if epsilon <= 0:
            printd('mvg_mechanism invalid input: Epsilon value {epsilon} <= 0',
                   epsilon=epsilon)
            valid = False
        if epsilon <= 0.1 or epsilon >= 2:
            printd('mvg_mechanism warning: Epsilon value {epsilon} is very small,\
                    or very large')
        if delta >= 0.25:
            printd('mvg_mechanism warning: Delta value {delta} is very large',
                   delta=delta)

        if covariance_direction == 'equimodal':
            printd('mvg_mechanism warning: equimodal covariance method \
            not yet implemented')
            valid = False
        return valid

    def generate_sample(self, X):
        if not(X.shape == self.shape):
            printd('mvg_mechanism input error: input data has shape {s1}, \
                    but mechanism requires shape {s2}',
                   s1=X.shape,
                   s2=self.shape)
        else:
            n, m = self.shape
            sample = numpy.array([numpy.random.normal(0, 1)
                                  for _ in range(n*m)]).reshape((n, m))

            if self.covariance_direction == 'unimodal features':
                s = numpy.matmul((identity(n) * sample),
                                 numpy.transpose(
                                 self.covariance['decomposition']))
            elif self.covariance_direction == 'unimodal observations':
                s = numpy.matmul(numpy.matmul(self.covariance['decomposition'],
                                              sample),
                                 numpy.identity(n))
            elif self.covariance_direction == 'equimodal':
                s = numpy.matmul(numpy.matmul(self.covariance['decomposition'],
                                              sample),
                                 numpy.transpose(
                                 self.covariance['decomposition']))
            return X + s
