import torch.nn as nn


class Model(nn.Module):
    name = "nunif.Model"
    def __init__(self, kwargs):
        super(Model, self).__init__()
        self.kwargs = {}
        self.updated_at = None
        self.register_kwargs(kwargs)

    def get_device(self):
        return next(self.parameters()).device

    def register_kwargs(self, kwargs):
        for name, value in kwargs.items():
            if name not in {"self"}:
                self.kwargs[name] = value

    def get_kwargs(self):
        return self.kwargs

    def get_config(self):
        return {}

    def __repr__(self):
        return (f"name: {self.name}\nkwargs: {self.kwargs}\n" +
                super(Model, self).__repr__())


class I2IBaseModel(Model):
    name = "nunif.i2i_base"

    def __init__(self, kwargs, scale, offset):
        super(I2IBaseModel, self).__init__(kwargs)
        self.i2i_scale = scale
        self.i2i_offset = offset

    def get_config(self):
        config = dict(super().get_config())
        config.update({"i2i_scale": self.i2i_scale, "i2i_offset": self.i2i_offset})
        return config
