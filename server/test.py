from threading import Thread
import asyncio


class testclass:
    ib = 0

    def test_async_func(self):
        def test_async_func2(self2):
            for i in range(0, 100):
                self2.ib += 1
                print("This is the second thread %s" % self2.ib)
        thread = Thread(target=test_async_func2, args=(self,))
        thread.start()
        return thread


obj = testclass()

a = obj.test_async_func()
for i in range(0, 100):
    obj.ib += 1
    print("And this is the first thread %s" % obj.ib)
