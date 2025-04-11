import setuptools

package_name = 'lade-gml'
version = '0.0.4'

if __name__ == '__main__':
    setuptools.setup(
        name=package_name,
        version=version,
        description='Lookahead Decoding Implementation',
        author='Fu Yichao',
        author_email='yichaofu2000@outlook.com',
        license='Apache-2',
        url='https://github.com/gimletlabs/LookaheadDecoding.git',
        packages=['lade', 'lade.models'],
        install_requires=[
            'transformers==4.36.2',
            'accelerate==0.23.0',
            'fschat==0.2.31',
            'openai',
            'anthropic',
            'einops==0.7.0',
            'torch<2.1.1'
        ]
    )

