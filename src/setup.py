from distutils.core import setup
import py2exe


option = {
    #'bundle_files':2,
    'compressed':True
}
setup(
    options = {'py2exe':option},
    console =['game.py'],
    zipfile = 'game.zip',
    )