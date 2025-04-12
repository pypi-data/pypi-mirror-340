from typing import Any
from baseTest import BaseTestCase
from jstreams import (
    BehaviorSubject,
    Flowable,
    PublishSubject,
    ReplaySubject,
    Single,
    rx_map,
    rx_filter,
    rx_reduce,
    rx_take,
    rx_take_while,
    rx_take_until,
    rx_drop_while,
    rx_drop_until,
    rx_drop,
)


class TestRx(BaseTestCase):
    def __init__(self, methodName="runTest"):
        super().__init__(methodName)
        self.val = None
        self.val2 = None

    def setVal(self, val: Any) -> None:
        self.val = val

    def addVal(self, val: Any) -> None:
        self.val.append(val)

    def addVal2(self, val: Any) -> None:
        self.val2.append(val)

    def test_single(self) -> None:
        self.val = None
        Single("test").subscribe(self.setVal)
        self.assertEqual(self.val, "test")

    def test_flowable(self) -> None:
        self.val = []
        init = ["test1", "test2"]
        Flowable(init).subscribe(self.addVal)
        self.assertListEqual(init, self.val)

    def test_behavior_subject(self) -> None:
        subject = BehaviorSubject("1")
        self.val = []
        sub = subject.subscribe(self.addVal)
        self.assertListEqual(
            self.val,
            ["1"],
            "BehaviorSubject should push the latest value on subscription",
        )
        subject.on_next("2")
        self.assertListEqual(
            self.val,
            ["1", "2"],
            "BehaviorSubject should push the latest value after subscription",
        )
        subject.on_next("3")
        self.assertListEqual(
            self.val,
            ["1", "2", "3"],
            "BehaviorSubject should push the latest value after subscription",
        )
        subject.pause(sub)
        subject.on_next("4")
        self.assertListEqual(
            self.val,
            ["1", "2", "3"],
            "BehaviorSubject should not push the latest value when subscription is paused",
        )
        subject.resume_paused()
        subject.on_next("5")
        self.assertListEqual(
            self.val,
            ["1", "2", "3", "5"],
            "BehaviorSubject should push the latest value when subscription is resumed",
        )
        subject.dispose()

    def test_publish_subject(self) -> None:
        subject = PublishSubject(str)
        self.val = []
        subject.on_next("1")
        sub = subject.subscribe(self.addVal)
        self.assertListEqual(
            self.val,
            [],
            "PublishSubject should not push the latest value on subscription",
        )
        subject.on_next("2")
        self.assertListEqual(
            self.val,
            ["2"],
            "PublishSubject should push the latest value after subscription",
        )
        subject.on_next("3")
        self.assertListEqual(
            self.val,
            ["2", "3"],
            "PublishSubject should push the latest value after subscription",
        )
        subject.pause(sub)
        subject.on_next("4")
        self.assertListEqual(
            self.val,
            ["2", "3"],
            "PublishSubject should not push the latest value when subscription is paused",
        )
        subject.resume_paused()
        subject.on_next("5")
        self.assertListEqual(
            self.val,
            ["2", "3", "5"],
            "PublishSubject should push the latest value when subscription is resumed",
        )
        subject.dispose()

    def test_replay_subject(self) -> None:
        subject = ReplaySubject(["A", "B", "C"])
        self.val = []
        self.val2 = []
        sub1 = subject.subscribe(self.addVal)
        self.assertListEqual(self.val, ["A", "B", "C"])
        subject.on_next("1")
        self.assertListEqual(self.val, ["A", "B", "C", "1"])
        sub2 = subject.subscribe(self.addVal2)
        self.assertListEqual(self.val2, ["A", "B", "C", "1"])
        subject.dispose()

    def test_replay_subject_map(self) -> None:
        subject = ReplaySubject(["a1", "a2", "a3"])
        self.val = []
        subject.pipe(rx_map(str.upper)).subscribe(self.addVal)
        self.assertListEqual(self.val, ["A1", "A2", "A3"])
        subject.on_next("a4")
        self.assertListEqual(self.val, ["A1", "A2", "A3", "A4"])
        subject.dispose()

    def test_replay_subject_filter(self) -> None:
        subject = ReplaySubject(["a1", "a2", "a3", "b", "c", "a4"])
        self.val = []
        subject.pipe(rx_filter(lambda s: s.startswith("a"))).subscribe(self.addVal)
        self.assertListEqual(self.val, ["a1", "a2", "a3", "a4"])
        subject.on_next("a5")
        self.assertListEqual(self.val, ["a1", "a2", "a3", "a4", "a5"])
        subject.on_next("b")
        self.assertListEqual(self.val, ["a1", "a2", "a3", "a4", "a5"])
        subject.dispose()

    def test_replay_subject_map_and_filter(self) -> None:
        subject = ReplaySubject(["a1", "a2", "a3"])
        self.val = []
        pipe1 = subject.pipe(rx_map(str.upper), rx_filter(lambda s: s.endswith("3")))
        pipe1.subscribe(self.addVal)
        self.assertListEqual(self.val, ["A3"])
        subject.on_next("a4")
        self.assertListEqual(self.val, ["A3"])
        subject.dispose()

    def test_replay_subject_map_and_filter_multiple(self) -> None:
        subject = ReplaySubject(["a1", "a2", "a3"])
        self.val = []
        pipe1 = subject.pipe(
            rx_map(str.upper),
            rx_filter(lambda s: s.endswith("3")),
            rx_map(lambda s: s + "Test"),
        )
        pipe1.subscribe(self.addVal)
        self.assertListEqual(self.val, ["A3Test"])
        subject.on_next("a4")
        self.assertListEqual(self.val, ["A3Test"])
        subject.dispose()

    def test_replay_subject_filter_and_reduce(self) -> None:
        subject = ReplaySubject([1, 7, 20, 5, 100, 40])
        self.val = []
        pipe1 = subject.pipe(
            rx_filter(lambda nr: nr <= 10), rx_reduce(lambda a, b: max(a, b))
        )
        pipe1.subscribe(self.addVal)
        self.assertListEqual(self.val, [1, 7])
        subject.on_next(9)
        self.assertListEqual(self.val, [1, 7, 9])
        subject.dispose()

    def test_replay_subject_with_take(self) -> None:
        subject = ReplaySubject([1, 7, 20, 5, 100, 40])
        self.val = []
        pipe1 = subject.pipe(rx_take(int, 3))
        pipe1.subscribe(self.addVal)
        self.assertListEqual(self.val, [1, 7, 20])
        subject.on_next(9)
        self.assertListEqual(self.val, [1, 7, 20])
        subject.dispose()

    def test_replay_subject_with_takeWhile(self) -> None:
        subject = ReplaySubject([1, 7, 20, 5, 100, 40])
        self.val = []
        pipe1 = subject.pipe(rx_take_while(lambda v: v < 10))
        pipe1.subscribe(self.addVal)
        self.assertListEqual(self.val, [1, 7])
        subject.on_next(9)
        self.assertListEqual(self.val, [1, 7])
        subject.dispose()

    def test_replay_subject_with_takeUntil(self) -> None:
        subject = ReplaySubject([1, 7, 20, 5, 100, 40])
        self.val = []
        pipe1 = subject.pipe(rx_take_until(lambda v: v > 10))
        pipe1.subscribe(self.addVal)
        self.assertListEqual(self.val, [1, 7])
        subject.on_next(9)
        self.assertListEqual(self.val, [1, 7])
        subject.dispose()

    def test_replay_subject_with_drop(self) -> None:
        subject = ReplaySubject([1, 7, 20, 5, 100, 40])
        self.val = []
        pipe1 = subject.pipe(rx_drop(int, 3))
        pipe1.subscribe(self.addVal)
        self.assertListEqual(self.val, [5, 100, 40])
        subject.on_next(9)
        self.assertListEqual(self.val, [5, 100, 40, 9])
        subject.dispose()

    def test_replay_subject_with_dropWhile(self) -> None:
        subject = ReplaySubject([1, 7, 20, 5, 100, 40])
        self.val = []
        pipe1 = subject.pipe(rx_drop_while(lambda v: v < 100))
        pipe1.subscribe(self.addVal)
        self.assertListEqual(self.val, [100, 40])
        subject.on_next(9)
        self.assertListEqual(self.val, [100, 40, 9])
        subject.dispose()

    def test_replay_subject_with_dropUntil(self) -> None:
        subject = ReplaySubject([1, 7, 20, 5, 100, 40])
        self.val = []
        pipe1 = subject.pipe(rx_drop_until(lambda v: v > 20))
        pipe1.subscribe(self.addVal)
        self.assertListEqual(self.val, [100, 40])
        subject.on_next(9)
        self.assertListEqual(self.val, [100, 40, 9])
        subject.dispose()

    def test_replay_subject_with_pipe_chaining(self) -> None:
        subject = ReplaySubject(range(1, 100))
        self.val = []
        self.val2 = []
        chainedPipe = (
            subject.pipe(rx_take_until(lambda e: e > 20))
            .pipe(rx_filter(lambda e: e % 2 == 0))
            .pipe(rx_take_while(lambda e: e < 10))
        )
        chainedPipe.subscribe(self.addVal)
        chainedPipe.subscribe(self.addVal2)
        chainedPipe.dispose()
        self.assertListEqual(self.val, [2, 4, 6, 8])
        self.assertListEqual(self.val2, [2, 4, 6, 8])
