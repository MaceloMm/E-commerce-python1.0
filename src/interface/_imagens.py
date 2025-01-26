from PIL import Image
from customtkinter import CTkImage
from src._functions import format_static_path

IMAGE_SINGUP = CTkImage(dark_image=Image.open(format_static_path('icon', 'add.png')).resize((15, 15)),
                        light_image=Image.open(format_static_path('icon', 'add.png')).resize((15, 15)),
                        size=(15, 15)
                        )

IMAGE_DELETE = CTkImage(dark_image=Image.open(format_static_path('icon', 'excluir.png')).resize((15, 15)),
                        light_image=Image.open(format_static_path('icon', 'excluir.png')).resize((15, 15)),
                        size=(15, 15)
                        )

IMAGE_ALTERAR = CTkImage(dark_image=Image.open(format_static_path('icon', 'refresh.png')).resize((15, 15)),
                         light_image=Image.open(format_static_path('icon', 'refresh.png')).resize((15, 15)),
                         size=(15, 15)
                         )

IMAGE_BACK = CTkImage(dark_image=Image.open(format_static_path('icon', 'previous.png')).resize((15, 15)),
                      light_image=Image.open(format_static_path('icon', 'previous.png')).resize((15, 15)),
                      size=(15, 15)
                      )

IMAGE_PRODUCT = CTkImage(dark_image=Image.open(format_static_path('icon', 'product.png')).resize((15, 15)),
                         light_image=Image.open(format_static_path('icon', 'product.png')).resize((15, 15)),
                         size=(15, 15)
                         )

IMAGE_GERENCIAL = CTkImage(dark_image=Image.open(format_static_path('icon', 'client_g.png')).resize((15, 15)),
                           light_image=Image.open(format_static_path('icon', 'client_g.png')).resize((15, 15)),
                           size=(15, 15)
                           )
IMAGE_ORDER = CTkImage(dark_image=Image.open(format_static_path('icon', 'orders.png')).resize((15, 15)),
                       light_image=Image.open(format_static_path('icon', 'orders.png')).resize((15, 15)),
                       size=(15, 15)
                       )