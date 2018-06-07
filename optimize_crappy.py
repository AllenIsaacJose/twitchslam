from helpers import add_ones
import autograd.numpy as np
from autograd import grad
from autograd import elementwise_grad as egrad
from scipy.optimize import least_squares, leastsq

def optimize(points):
  # get point location guesses (parameter vector)
  x0 = []
  for p in points:
    x0.append(p.pt)
  x0 = np.array(x0).flatten()

  # get target residuals (measurement vector)
  uvs = []
  for p in points:
    for f, idx in zip(p.frames, p.idxs):
      uv = f.kps[idx]
      uvs.append(uv)
  b = np.array(uvs).flatten()

  # compute residuals
  def res(x):
    ret = []
    for i, p in enumerate(points):
      for f, idx in zip(p.frames, p.idxs):
        proj = np.dot(f.pose[:3], add_ones(x[i*3:(i+1)*3]))
        ret.append(proj)
    ret = np.array(ret)
    ret = ret[:, 0:2] / ret[:, 2:]
    return ret.flatten()

  print(res(x0))
  print(b)
  exit(0)
  

  # define jacobian of function 
  J = np.zeros((x0.shape[0], b.shape[0]))
  # TODO: actually do this
  # http://www.cs.technion.ac.il/users/wwwb/cgi-bin/tr-get.cgi/2014/MSC/MSC-2014-16.pdf page 17
  # http://www.telesens.co/2016/10/13/bundle-adjustment-part-1-jacobians/ defines 2x3 jacobian

  # define function fun(parameter) = measurement

  def fun(x):
    def fun_loss(comp, meas):
      return np.sum((comp-meas)**2)
    return fun_loss(res(x), b)



  # stack poses
  grad_fun = grad(fun)
  print("computing at x0")

  # gradient descent
  for i in range(20):
    loss = fun(x0)
    d = grad_fun(x0)
    print(loss, d)
    x0 -= d

  """
  poses = []
  for i, p in enumerate(self.points):
    for f, idx in zip(p.frames, p.idxs):
      poses.append(f.pose[:3])
  poses = np.concatenate(poses, axis=1)
  print(poses.shape)

  loss = np.dot(poses, x0)
  print(loss)
  """

  print("running least squares with %d params" % len(x0))
  