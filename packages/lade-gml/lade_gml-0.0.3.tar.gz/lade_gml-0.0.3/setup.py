import setuptools

package_name = 'lade-gml'
version = '0.0.3'

if __name__ == '__main__':
    setuptools.setup(
        name=package_name,
        version=version,
        description='Lookahead Decoding Implementation',
        author='Fu Yichao',
        author_email='yichaofu2000@outlook.com',
        license='Apache-2',
        url='https://github.com/gimletlabs/LookaheadDecoding.git',
        packages=['lade', 'lade.models']
    )

