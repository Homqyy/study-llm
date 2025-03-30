import torch

a = torch.tensor([1.], requires_grad=True)
b = torch.tensor([2.], requires_grad=True)
c = a * b

c.backward()
print('a.grad:', a.grad, '; b.grad: ', b.grad);
