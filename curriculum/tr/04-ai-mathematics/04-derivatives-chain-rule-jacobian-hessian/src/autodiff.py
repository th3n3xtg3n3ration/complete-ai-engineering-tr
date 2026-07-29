"""A tiny reverse-mode automatic differentiation engine."""

from __future__ import annotations

from dataclasses import dataclass, field
from math import exp, log
from typing import Callable


@dataclass(eq=False)
class Value:
    data: float
    label: str = ""
    grad: float = 0.0
    _prev: tuple["Value", ...] = field(default_factory=tuple, repr=False)
    _backward: Callable[[], None] = field(default=lambda: None, repr=False)

    def __add__(self, other: float | "Value") -> "Value":
        rhs = other if isinstance(other, Value) else Value(float(other))
        output = Value(self.data + rhs.data, _prev=(self, rhs))

        def backward() -> None:
            self.grad += output.grad
            rhs.grad += output.grad

        output._backward = backward
        return output

    __radd__ = __add__

    def __mul__(self, other: float | "Value") -> "Value":
        rhs = other if isinstance(other, Value) else Value(float(other))
        output = Value(self.data * rhs.data, _prev=(self, rhs))

        def backward() -> None:
            self.grad += rhs.data * output.grad
            rhs.grad += self.data * output.grad

        output._backward = backward
        return output

    __rmul__ = __mul__

    def __neg__(self) -> "Value":
        return self * -1.0

    def __sub__(self, other: float | "Value") -> "Value":
        return self + (-other if isinstance(other, Value) else -float(other))

    def __rsub__(self, other: float | "Value") -> "Value":
        return other + (-self)

    def __truediv__(self, other: float | "Value") -> "Value":
        rhs = other if isinstance(other, Value) else Value(float(other))
        return self * rhs.pow(-1.0)

    def pow(self, exponent: float) -> "Value":
        output = Value(self.data**exponent, _prev=(self,))

        def backward() -> None:
            self.grad += exponent * (self.data ** (exponent - 1.0)) * output.grad

        output._backward = backward
        return output

    def tanh(self) -> "Value":
        e2x = exp(2.0 * self.data)
        value = (e2x - 1.0) / (e2x + 1.0)
        output = Value(value, _prev=(self,))

        def backward() -> None:
            self.grad += (1.0 - value * value) * output.grad

        output._backward = backward
        return output

    def relu(self) -> "Value":
        output = Value(max(0.0, self.data), _prev=(self,))

        def backward() -> None:
            self.grad += (1.0 if self.data > 0.0 else 0.0) * output.grad

        output._backward = backward
        return output

    def exp(self) -> "Value":
        value = exp(self.data)
        output = Value(value, _prev=(self,))

        def backward() -> None:
            self.grad += value * output.grad

        output._backward = backward
        return output

    def log(self) -> "Value":
        if self.data <= 0.0:
            raise ValueError("log input must be positive")
        output = Value(log(self.data), _prev=(self,))

        def backward() -> None:
            self.grad += output.grad / self.data

        output._backward = backward
        return output

    def backward(self) -> None:
        topology: list[Value] = []
        visited: set[Value] = set()

        def build(node: Value) -> None:
            if node in visited:
                return
            visited.add(node)
            for parent in node._prev:
                build(parent)
            topology.append(node)

        build(self)
        for node in topology:
            node.grad = 0.0
        self.grad = 1.0
        for node in reversed(topology):
            node._backward()


if __name__ == "__main__":
    x = Value(2.0, "x")
    w = Value(-3.0, "w")
    target = Value(1.0, "target")
    prediction = (x * w + 0.5).tanh()
    loss = (prediction - target).pow(2.0)
    loss.backward()
    print({"loss": loss.data, "dx": x.grad, "dw": w.grad})
