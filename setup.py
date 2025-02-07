from setuptools import setup

setup(
    name='maxim',
    install_requires=[
        'complexpbr'  # Ensure complexpbr is installed
    ],
    packages=['complexpbr'],
    options={
        'build_apps': {
            # Build asteroids.exe as a GUI application
            'gui_apps': {
                'maxim': 'main.py',
            },
            "icons": {
                # The key needs to match the key used in gui_apps/console_apps.
                # Alternatively, use "*" to set the icon for all apps.
                "maxim": ["maxim.jpg"],
            },

            # Set up output logging, important for GUI apps!
            'log_filename': '$USER_APPDATA/Maxim/output.log',
            'log_append': False,

            # Specify which files are included with the distribution
            'include_patterns': [
                '**/*.png',
                '**/*.jpg',
                '**/*.egg',
                '**/*.wav',
                '**/*.bam',
                '**/*.mp3',
                '**/*.vert',
                '**/*.frag',
                '**/*.glsl',
                '**/*.prc',
                '**/*.shader',
                '**/*.egg.pz',
                '**/*.tif',
                'maps/*',
                'Lib/complexpbr/*.vert',  # Include complexpbr shaders
                'Lib/complexpbr/*.frag',

            ],
            # Include the OpenGL renderer and OpenAL audio plug-in
            'plugins': ['pandagl', 'p3openal_audio', 'p3ffmpeg', 'p3fmod_audio'],
            # Include the complexpbr module and its dependencies
            'include_modules': {
                '*': ['complexpbr'],

            },

        }
    }
)
