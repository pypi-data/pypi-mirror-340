from setuptools import find_packages, setup

setup(
    name="gigaam",
    py_modules=["gigaam"],
    version="0.1.0",
    description="GigaAM: A package for audio modeling and ASR.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    readme="README.md",
    author="GigaChat Team",
    url="https://github.com/salute-developers/GigaAM/",
    license="MIT",
    packages=find_packages(include=["gigaam"]),
    python_requires=">=3.8",
    install_requires=[
        'hydra-core<=1.3.2',
        'numpy',
        'omegaconf<=2.3.0',
        'pydub<=0.25.1',
        'sentencepiece<=0.2.0',
        'torch<=2.5.1',
        'torchaudio<= 2.5.1',
        'onnx==1.17.0',
        'onnxruntime==1.17.3',
        'tqdm'
    ],
    extras_require={"longform": ["pyannote.audio", "pydub"]},
    include_package_data=True,
)
