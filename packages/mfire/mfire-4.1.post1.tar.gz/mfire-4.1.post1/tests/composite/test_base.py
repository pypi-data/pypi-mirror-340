from functools import cached_property
from typing import List
from unittest.mock import patch

import pytest

import mfire.utils.mfxarray as xr
from mfire.composite.base import BaseComposite, precached_property
from mfire.utils.xr import ArrayLoader
from tests.composite.factories import BaseCompositeFactory
from tests.functions_test import assert_identically_close


class TestBaseComposite:
    basic_data = xr.DataArray([1, 2, 3])

    def test_cached_attrs(self):
        assert not BaseCompositeFactory().cached_attrs

    def test_make_copy(self):
        # Test of deep=True argument in make_copy
        class BaseCompositeTest(BaseCompositeFactory):
            a: list = [1, 2]

        obj1 = BaseCompositeTest()
        obj2 = obj1.make_copy()
        obj1.a.append(3)
        assert obj2.a == [1, 2]

    def test_handle_children(self):
        # Test when the shared config is given to children
        class BaseCompositeTest(BaseComposite):
            _shared_config: dict = {}
            obj: BaseComposite = BaseComposite()
            objs: List[BaseComposite] = [BaseComposite(), BaseComposite()]

        composite = BaseCompositeTest()
        composite.shared_config["a"] = "b"
        assert composite.obj.parent is not None
        assert composite.obj.shared_config == {"a": "b"}
        assert composite.objs[0].shared_config == {"a": "b"}
        assert composite.objs[1].shared_config == {"a": "b"}
        assert composite.objs[0] is not None
        assert composite.objs[1] is not None

        # Test when the parent is already defined
        class BaseCompositeTestChild(BaseComposite):
            parent: BaseComposite = BaseCompositeFactory(
                shared_config_factory={"a": "b"}
            )

        class BaseCompositeTest(BaseComposite):
            shared_config: dict = {"c": "d"}
            obj: BaseCompositeTestChild = BaseCompositeTestChild()

        assert BaseCompositeTest().obj.parent.shared_config == {"a": "b"}

    def test_time_zone(self):
        composite = BaseCompositeFactory(shared_config_factory={"time_zone": "XXX"})
        assert composite.time_zone == "XXX"

    def test_language(self):
        composite = BaseCompositeFactory(shared_config_factory={"language": "XXX"})
        assert composite.language == "XXX"

    def test_set_language(self):
        composite = BaseCompositeFactory(
            shared_config_factory={"language": "XXX", "translation": ...}
        )
        composite.set_language("YYY")
        assert composite.language == "YYY"
        assert "translation" not in composite.shared_config

    def test_translation(self):
        composite = BaseCompositeFactory()

        assert {
            language: composite._("en dessous de")
            for language in composite.iter_languages()
        } == {"fr": "en dessous de", "en": "under", "es": "por debajo"}

    def test_data(self):
        composite = BaseCompositeFactory()
        assert composite._data is None
        composite._data = self.basic_data
        assert_identically_close(composite._data, self.basic_data)

    def test_hash(self, assert_equals_result):
        assert_equals_result(BaseCompositeFactory().hash)

    def test_reset(self):
        # Test deletion of self._data
        composite = BaseCompositeFactory(cached_attrs_factory={"data": ArrayLoader})
        composite._data = self.basic_data
        composite.reset()

        assert composite.compute() is None

        # Test of deletion of cache
        path = composite.cached_filename("data")
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w") as file:
            file.close()

        assert path.exists()
        composite.reset()
        assert not path.exists()

        # Test of translation and children reset
        class TestBaseCompositeFactoryChild(BaseCompositeFactory):
            a: int = 1

            def reset(self):
                super().reset()
                self.a = 2

        class TestBaseCompositeFactoryParent(TestBaseCompositeFactoryChild):
            child: TestBaseCompositeFactoryChild = TestBaseCompositeFactoryChild()
            children: List[TestBaseCompositeFactoryChild] = [
                TestBaseCompositeFactoryChild(),
                TestBaseCompositeFactoryChild(),
            ]

        composite = TestBaseCompositeFactoryParent(
            shared_config_factory={"translation": ...}
        )
        composite.reset()

        assert composite.a == 2
        assert composite.child.a == 2
        assert composite.children[0].a == 2
        assert composite.children[1].a == 2

        # Test of reset of cached and precached properties
        class TestBaseCompositeFactory(BaseCompositeFactory):
            a: int = 0
            b: int = 0

            @cached_property
            def f1(self):
                self.a += 1
                return self.a

            @precached_property
            def f2(self):
                self.b += 1
                return self.b

        composite = TestBaseCompositeFactory()
        assert composite.f1 == 1
        assert composite.f1 == 1
        assert composite.f2 == 1
        assert composite.f2 == 1

        composite.reset()
        assert composite.f1 == 2
        assert composite.f2 == 2

    def test_is_cached(self):
        composite = BaseCompositeFactory(cached_attrs_factory={"data": ArrayLoader})
        assert composite.is_cached is False

        path = composite.cached_filename("data")
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w") as file:
            file.close()
        assert composite.is_cached is True

        composite.factories["cached_attrs"] = {}
        assert composite.is_cached is False

    def test_load_cache(self, tmp_path_cwd):
        composite = BaseCompositeFactory(cached_attrs_factory={"data": ArrayLoader})
        with pytest.raises(
            FileNotFoundError,
            match="BaseCompositeFactory not cached, you must compute it before.",
        ):
            composite.load_cache()

        path = composite.cached_filename("data")
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, mode="w") as f:
            f.close()

        assert composite.load_cache() is False
        assert composite._data is None

        self.basic_data.to_netcdf(path)
        assert composite.load_cache() is True
        assert_identically_close(composite._data, self.basic_data)

    def test_dump_cache(self, tmp_path_cwd):
        output_folder = tmp_path_cwd / "cache" / "BaseCompositeFactory"

        # Fail to dump
        composite = BaseCompositeFactory(cached_attrs_factory={"data": ArrayLoader})
        composite.dump_cache()
        assert len(list(output_folder.iterdir())) == 0

        # Dump basic data
        composite._data = self.basic_data
        composite.dump_cache()

        assert output_folder.exists()
        output_file = list(output_folder.iterdir())
        assert len(output_file) == 1
        assert_identically_close(xr.open_dataarray(output_file[0]), self.basic_data)

    def test_compute(self, tmp_path_cwd):
        # Behavior by default: data are not kept
        composite = BaseCompositeFactory(cached_attrs_factory={"data": ArrayLoader})
        composite._data = self.basic_data
        assert_identically_close(composite.compute(), self.basic_data)
        assert composite.compute() is None

        # When data are kept
        composite._data = self.basic_data
        composite._keep_data = True
        assert_identically_close(composite.compute(), self.basic_data)
        assert_identically_close(composite.compute(), self.basic_data)

        # Test the kwargs _keep_data
        composite = BaseCompositeFactory(cached_attrs_factory={"data": ArrayLoader})
        composite._data = self.basic_data
        assert_identically_close(composite.compute(keep_data=True), self.basic_data)
        assert_identically_close(composite.compute(), self.basic_data)
        assert composite.compute() is None

        # Test the dumping kwargs possibility
        assert not (tmp_path_cwd / "cache").exists()
        composite = BaseCompositeFactory(cached_attrs_factory={"data": ArrayLoader})

        with patch(
            "mfire.composite.base.BaseComposite._compute",
            lambda *args, **kwargs: self.basic_data,
        ):
            composite.compute(save_cache=True)
            output_file = list(
                (tmp_path_cwd / "cache" / "BaseCompositeFactory").iterdir()
            )
            assert len(output_file) == 1
            assert_identically_close(xr.open_dataarray(output_file[0]), self.basic_data)
