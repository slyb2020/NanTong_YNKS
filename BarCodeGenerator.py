# code128
from pystrich.code128 import Code128Encoder

code = '64757-0001'
encoder = Code128Encoder(code)
encoder.save("code128.png", bar_width=2)
