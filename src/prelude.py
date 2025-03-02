import hashlib
import os
import pickle


def uniq(xs):
    return list(dict.fromkeys(xs))


class Logger:
    def ignore(*args, **kwargs):
        pass

    def __init__(self):
        self.moderate()

    def verbose(self):
        self.info_ = print
        self.say_ = print
        self.warn_ = print

    def quiet(self):
        self.info_ = Logger.ignore
        self.say_ = Logger.ignore
        self.warn_ = print

    def moderate(self):
        self.info_ = Logger.ignore
        self.say_ = print
        self.warn_ = print

    def say(self, msg):
        self.say_(msg, flush=True)

    def info(self, msg):
        self.info_(msg, flush=True)

    def warn(self, msg):
        self.warn_("\U0001f4a3 " + msg)


logger = Logger()


class Store:
    def __init__(self, key, root=None):
        if root:
            self.root = root
        else:
            self.root = "tmp/store"
        self.out = f"{self.root}/{Store.digest(Store.compact(key))}"

    def put(self, path, obj):
        file = f"{self.out}/{path}"
        dir = os.path.dirname(file)
        os.makedirs(dir, exist_ok=True)
        with open(f"{self.out}/{path}", "wb") as f:
            pickle.dump(obj, f)

    def get(self, path):
        file = f"{self.out}/{path}"
        if os.path.exists(file):
            try:
                with open(file, "rb") as f:
                    return pickle.load(f)
            except Exception:
                pass
        return None

    def compact(key):
        return [(k, v) for (k, v) in key if v is not None]

    def digest(obj):
        return hashlib.md5(str(obj).encode("utf-8")).hexdigest()

    disabled = False

    def disable():
        Store.disabled = True


def with_store(key, path, fn, force=False, exceptional=False):
    """
    Args:
      force:
        If True, skips to read the store, forces to evaluate the fn and stores the result.
      exceptional:
        If True, stores exceptions and reproduces them when a stored object is an exception.
    """
    if Store.disabled:
        return fn()

    store = Store(key)
    obj = None
    if force:
        logger.info(f"Store force: {store.out}/{path}")
    else:
        obj = store.get(path)
        if obj:
            logger.info(f"Store hit: {store.out}/{path}")
        else:
            logger.info(f"Store miss: {store.out}/{path}")
        if obj:
            if type(obj) is Exception:
                if exceptional:
                    raise obj
            else:
                return obj
    try:
        obj = fn()
        store.put(path, obj)
    except Exception as e:
        if exceptional:
            store.put(path, e)
        raise e
    return obj


def read_store(key, path):
    return Store(key).get(path)
