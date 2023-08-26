# coding=utf-8
# data：2023/8/25-14:14

# 密钥
JWT_SECRET: str = "Z+ML7m0xDCETanJdl69RIJhGuQJNjLVVFBgcCyZUW0E="
# 过期时间
JWT_EXPIRATION_DELTA_SECONDS = 7 * 24 * 60 * 60
# token 应该放在哪个header
JWT_AUTH_HEADER = "Authorization"
# token格式 Bearer token_content
JWT_AUTH_HEADER_PREFIX = "bearer"
