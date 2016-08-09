import numpy as np
from position import Location
from astropy.modeling import fitting, models, Parameter, Fittable1DModel
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


# Assymetric guassian function
class AGaussian1D(Fittable1DModel):
    inputs = ('x',)
    outputs = ('y',)

    amplitude = Parameter()
    x0 = Parameter()
    l_sig = Parameter()
    r_sig = Parameter()

    @staticmethod
    def evaluate(x, amplitude, x0, l_sig, r_sig):
        sig = np.where(x < x0, l_sig, r_sig)
        f = models.Gaussian1D(amplitude, x0, sig)
        return f(x)


def hist_fit_single(rmid):
    hist_file = Location.project_loca + "result/light_curve/" + str(rmid) + \
        "/cont-hbeta.txt"
    fit_file = Location.project_loca + "result/light_curve/" + str(rmid) + \
        "/javelin_lag.txt"
    fit_img = Location.project_loca + "result/light_curve/" + str(rmid) + \
        "/lag_fit.eps"
    hist_data = np.loadtxt(hist_file)
    lag = hist_data[:, 2]
    hist, x = np.histogram(lag, 500)
    fitter = fitting.LevMarLSQFitter()
    func = AGaussian1D(max(hist), x[np.argmax(hist)], 1.0, 1.0)
    fit = fitter(func, x[0: 500], hist, maxiter=10000)
    np.savetxt(fit_file, fit.parameters)
    fig = plt.figure()
    plt.hist(lag, 500)
    plt.plot(x, fit(x))
    fig.savefig(fit_img, format='eps')
    plt.close()


def hist_fit(rmid):
    print("Begining time lag hist fit for " + str(rmid))
    try:
        hist_fit_single(rmid)
        print("Finished")
    except Exception as reason:
        print(str("Failed: ") + str(reason))
