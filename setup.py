from setuptools import setup

setup(
    name='maxim',
    options={
        'build_apps': {
            # Build asteroids.exe as a GUI application
            'gui_apps': {
                'maxim': 'main.py',
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



            ],

            "gui_apps": {
    "main": "src/main.py",
},
"icons": {
    # The key needs to match the key used in gui_apps/console_apps.
    # Alternatively, use "*" to set the icon for all apps.
    "maxim": ["maxim.png"],
},

            # Include the OpenGL renderer and OpenAL audio plug-in
            'plugins': [
                'pandagl',
                'p3openal_audio',
            ],
        }
    }
)

# python setup.py build_apps