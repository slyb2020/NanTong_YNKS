# code128
from pystrich.code128 import Code128Encoder

code = '64757-01A'
encoder = Code128Encoder(code)
encoder.save("code128.png", bar_width=2)
