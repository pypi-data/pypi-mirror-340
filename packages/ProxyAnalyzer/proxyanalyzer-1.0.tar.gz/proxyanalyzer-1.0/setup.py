from setuptools import setup

setup(
    name='ProxyAnalyzer',
    version='1.0',
    py_modules=['proxy_app', 'proxy_server'],  # استخدم py_modules بدلاً من packages
    install_requires=[
        'mitmproxy',
    ],
    entry_points={
        'console_scripts': [
            'proxy-analyzer = proxy_app:main',  # تأكد أن proxy_app.py فيه دالة main()
        ],
    },
)
