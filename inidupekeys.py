import argparse
import configparser

from configparser import DuplicateOptionError
from configparser import RawConfigParser
from collections import defaultdict

class defaultdict_factory(defaultdict):

    def __init__(self, factory=list, *args, **kwargs):
        super().__init__(factory, *args, **kwargs)

    def __setitem__(self, item, value):
        """
        Convert set items to extending the list.
        """
        # `RawConfigParser._read` wraps `value` in a list for options.
        if isinstance(value, list):
            if item not in self.__dict__:
                self.__dict__[item] = self.default_factory()
            self.__dict__[item].extend(value)
            print(f'{locals()=}')
        else:
            super().__setitem__(item, value)


class MultipleConfigParser(RawConfigParser):
    """
    Consume duplicate options as list.
    """
    # NOTES
    # * RawConfigParser bypasses its own machinery for adding sections
    # * it maintains an `elements_added` for raising duplicate sections inside
    #   the huge `RawConfigParser._read` method.
    # * strict = False allows duplicate options
    # * uses one dict factory for everything. we want to treat options
    #   specially and append-on-set.
    # * `._dict` is used to create new sections in `._read`
    # * XXX: 2021-10-17 lost hope that subclassing RawConfigParser to
    #        automatically consume duplicate options is not possible without
    #        doing horrible things.

    def __init__(self, **super_kwargs):
        # non-strict to ignore duplicate options
        strict = False
        # we set _dict after super init so that super can create _sections and
        # _defaults and ours is used inside _read
        super().__init__(strict=strict, **super_kwargs)
        self._dict = defaultdict_factory


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('config')
    args = parser.parse_args(argv)

    # NOTES
    # * using RawConfigParser with strict=False, allows this but only the last
    #   consumed option is set.

    class_ = MultipleConfigParser
    #class_ = RawConfigParser
    cp = class_()
    cp.read(args.config)

    print('***')
    for section_name in cp.sections():
        print(section_name, f'{cp[section_name]=}')
        breakpoint()
        for option, value in cp[section_name].items():
            print(option, value)

if __name__ == '__main__':
    main()
