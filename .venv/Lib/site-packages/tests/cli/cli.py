
from unittest import TestCase

from pydantic import BaseModel, Field

from mapping_shortcuts.cli import cli_handler, run_args, help_handler
from mapping_shortcuts.cli.cli import CMD_HANDLERS


class RunCliTestCase(TestCase):
    def test_simple(self):
        CMD_HANDLERS.clear()
        cmd1 = False
        cmd2 = False

        @cli_handler('cmd1')
        def handler(args):
            nonlocal cmd1
            cmd1 = True

        @cli_handler('cmd2')
        def handler(args):
            nonlocal cmd2
            cmd2 = True

        assert len(CMD_HANDLERS) == 2
        run_args(['cmd1'])
        self.assertTrue(cmd1)
        self.assertFalse(cmd2)

    def test_empty_run(self):
        CMD_HANDLERS.clear()
        cmd1 = 0

        @cli_handler('help')
        def handler(args):
            nonlocal cmd1
            cmd1 += 1

        assert len(CMD_HANDLERS) == 1
        run_args([])
        run_args(['-?'])
        run_args(['-h'])
        run_args(['--help'])
        self.assertEqual(cmd1, 4)

    def test_run_help(self):
        CMD_HANDLERS.clear()

        cli_handler('help')(help_handler)

        assert len(CMD_HANDLERS) == 1
        run_args([])
        # should not raise exceptions

    def test_model(self):
        CMD_HANDLERS.clear()

        class ArgModel(BaseModel):
            param1: str = Field(alias='--param1')
            param2: str = Field(alias='-p2')

        cmd1 = False

        @cli_handler('cmd1', model=ArgModel)
        def handler(args: ArgModel):
            nonlocal cmd1
            self.assertTrue(args.param2)
            self.assertEqual(args.param1, '123')
            cmd1 = True

        assert len(CMD_HANDLERS) == 1
        try:
            run_args(['cmd1'])
            self.assertTrue(False, 'expected exception')
        except ValueError:
            ...

        run_args(['cmd1', '--param1=123', '-p2'])
        self.assertTrue(cmd1)

    def test_annotation(self):
        CMD_HANDLERS.clear()

        class ArgModel1(BaseModel):
            param: str = Field(alias='--param')

        class ArgModel2(BaseModel):
            param: str = Field(alias='--param')

        @cli_handler('cmd1', model=ArgModel1)
        def handler_1(args):
            ...

        @cli_handler('cmd2')
        def handler_2(args: ArgModel2):
            ...

        assert len(CMD_HANDLERS) == 2
        self.assertIs(CMD_HANDLERS['cmd1'].func, handler_1)
        self.assertIs(CMD_HANDLERS['cmd1'].model, ArgModel1)
        self.assertIs(CMD_HANDLERS['cmd2'].func, handler_2)
        self.assertIs(CMD_HANDLERS['cmd2'].model, ArgModel2)

    def test_list_args(self):
        CMD_HANDLERS.clear()

        class ArgModel(BaseModel):
            param: list[int] = Field(alias='--param')

        @cli_handler('cmd1')
        def handler_1(args: ArgModel):
            self.assertEqual(args.param, [123, 456])

        @cli_handler('cmd2')
        def handler_2(args: ArgModel):
            self.assertEqual(args.param, [123])

        assert len(CMD_HANDLERS) == 2
        self.assertIs(CMD_HANDLERS['cmd1'].func, handler_1)
        self.assertIs(CMD_HANDLERS['cmd2'].func, handler_2)
        run_args(['cmd1', '--param=123', '--param=456'])
        run_args(['cmd2', '--param=123'])
