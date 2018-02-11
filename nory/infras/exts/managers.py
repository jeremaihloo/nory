"""
__auth__
"""
import logging
import os
from nory.infras.exts import features
from nory.infras.exts.info_loaders import load_extension_info
from nory.infras.exts.dependency import sort_extension_dependency
from nory.infras.exts.models import Extension


def get_extensions_paths():
    abs_p = os.path.abspath('.')
    extensions = os.listdir(os.path.join(abs_p, 'extensions'))

    extensions = list(filter(lambda x: not x.startswith('_') and not x.startswith('.') and not x.endswith('.py'), extensions))
    return extensions


class ExtensionManager(object):
    def __init__(self, extension=None):
        self.extension = extension
        self.extensions = {}

    async def reload_extensions(self):

        await self.load_extensions()

    async def do_extension_loading(self):
        enabled_extensions = self.get_enabled_extensions()
        for extension in enabled_extensions:
            await extension.on_installing()

    async def load_extensions(self):
        logging.info('start loading extensions')
        extension_names = get_extensions_paths()

        extension_infos = await self.load_extension_infos(extension_names)
        extensions = await self.load_extension_entries(extension_infos)

        await self.do_extension_loading()
        return extensions

    async def load_extension_infos(self, extension_names):
        extension_infos = []
        for item in extension_names:
            try:
                info = load_extension_info(item)
                if info:
                    extension_infos.append(info)
                    logging.debug('[load_extension_info] found loader for [{}]'.format(item))
            except Exception as e:
                logging.exception('[load_extension_infos] load extension info [{}] error', item, e)
        extension_infos = sort_extension_dependency(extension_infos)

        logging.info('[load_extension_infos] sorted extension info dependency [{}]'.format([x.name for x in extension_infos]))
        return extension_infos

    async def load_extension_entries(self, extension_infos):
        for item in extension_infos:
            extension = Extension(item, self.extension)

            if item.name:
                item.enabled = True
            try:
                if item.enabled:
                    await extension.load()
                    self.extensions[item.name] = extension
                    logging.info('[load_extensions] extension [{}] loaded'.format(item.name))
                else:
                    logging.info('[load_extensions] extension [{}] skiped [disabled]'.format(item.name))
            except Exception as e:
                logging.exception('[load_extensions] extension [{}] load error'.format(item.name))

    def get_enabled_extensions(self):
        enabled_extensions = [x for x in self.extensions.values() if x.info.enabled]
        return enabled_extensions

    def get_worked_features(self, event):
        enabled_extensions = self.get_enabled_extensions()
        fs = []
        for item in enabled_extensions:
            enabled_features = item.get_worked_features(event)
            fs.extend(enabled_features)
        logging.debug('[get_worked_features] {}'.format(features))
        return fs
