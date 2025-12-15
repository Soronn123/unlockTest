import os

TYPE_FILE = "txt"

class LogClass:
    def __init__(self):
        self.current_path = "c:\\users\\{}\\Desktop".format(os.getenv("username"))
        self.current_name = "new"

        target = self.create_name(self.current_name)
        if not os.path.exists(target):
            with open(target, 'w'):
                pass

    def create_name(self, name):
        return os.path.join(self.current_path, name + "." + TYPE_FILE)

    def rename(self, new_name:str):
        old_target = self.create_name(self.current_name)
        new_target = self.create_name(new_name)

        if old_target == new_target:
            return

        if os.path.exists(new_target):
            self.delete_file(old_target)
        else:
            os.rename( old_target, new_target )
        self.current_name = new_name

    def delete_file(self, file) -> None:
        os.remove(file)

    def stop(self) -> None:
        self.delete_file(
            self.create_name(self.current_name)
        )

class AsynLogClass:
    def __init__(self):
        self.current_path = "c:\\users\\{}\\Desktop".format(os.getenv("username"))
        self.current_name = "tg"

        target = os.path.join(self.current_path, self.current_name + "." + TYPE_FILE)
        if not os.path.exists(target):
            with open(target, 'w'):
                pass

    async def create_name(self, name):
        return os.path.join(self.current_path, name + "." + TYPE_FILE)

    async def rename(self, new_name:str):
        old_target = await self.create_name(self.current_name)
        new_target = await self.create_name(new_name)

        if old_target == new_target:
            return


        if os.path.exists(new_target):
            await self.delete_file(old_target)
        else:
            os.rename( old_target, new_target )
        self.current_name = new_name

    async def delete_file(self, file) -> None:
        os.remove(file)

    async def stop(self) -> None:
        await self.delete_file(
            await self.create_name(self.current_name)
        )
