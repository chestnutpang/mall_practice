from sanic.response import json
from model import User


def check_captcha(phone, captcha):
    return True


async def register(request):
    params = request.json
    phone = params.get('phone')
    captcha = params.get('captcha')
    password = params.get('password')

    if not check_captcha(phone, captcha):
        pass

    user = await User().register(request, {
        'username': phone,
        'password': password,
        'nickname': phone
    })
    return json({
        'username': user.username,
        'nickname': user.nickname
    })


async def login(request):
    params = request.json
    phone = params.get('phone')
    password = params.get('password')
    res = await User().login(request, phone, password)
    if res is None:
        return json({})

    return json(res)


async def logout(request):
    await User().logout(request)
    return json({})


async def user_info(request):
    res = await User.get_user_info(request)
    return json(res)
