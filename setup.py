from distutils.core import setup

setup(
    name='django-sugar',
    version='0.2',
    license='BSD',
    description='Curated collection of all the sweet Django helpers/utilities \
        developers create, and sometimes recreate too often.',
    author='Kevin Fricovsky',
    author_email='kfricovsky@gmail.com',
    url='http://github.com/montylounge/django-sugar/tree',
    packages=[
        'sugar',
        'sugar.admin',
        'sugar.cache',
        'sugar.forms',
        'sugar.middleware',
        'sugar.templatetags',
        'sugar.views',
        'sugar.widgets',
        'sugar.utils',
    ],
    classifiers=[
        'Development Status :: 2 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)

