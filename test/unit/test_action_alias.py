from unittest import TestCase
from mock import Mock, patch
import elasticsearch
import curator
# Get test variables and constants from a single source
from . import testvars as testvars

class TestActionAlias(TestCase):
    def test_init_raise(self):
        self.assertRaises(curator.MissingArgument, curator.Alias)
    def test_add_raises_on_missing_parameter(self):
        client = Mock()
        client.indices.get_settings.return_value = testvars.settings_one
        client.cluster.state.return_value = testvars.clu_state_one
        client.indices.stats.return_value = testvars.stats_one
        ilo = curator.IndexList(client)
        ao = curator.Alias(alias='alias')
        self.assertRaises(TypeError, ao.add)
    def test_add_raises_on_invalid_parameter(self):
        client = Mock()
        client.indices.get_settings.return_value = testvars.settings_one
        client.cluster.state.return_value = testvars.clu_state_one
        client.indices.stats.return_value = testvars.stats_one
        ilo = curator.IndexList(client)
        ao = curator.Alias(alias='alias')
        self.assertRaises(TypeError, ao.add, [])
    def test_add_single(self):
        client = Mock()
        client.indices.get_settings.return_value = testvars.settings_one
        client.cluster.state.return_value = testvars.clu_state_one
        client.indices.stats.return_value = testvars.stats_one
        ilo = curator.IndexList(client)
        ao = curator.Alias(alias='alias')
        ao.add(ilo)
        self.assertEqual(testvars.alias_one_add, ao.actions)
    def test_remove_single(self):
        client = Mock()
        client.indices.get_settings.return_value = testvars.settings_one
        client.cluster.state.return_value = testvars.clu_state_one
        client.indices.stats.return_value = testvars.stats_one
        ilo = curator.IndexList(client)
        ao = curator.Alias(alias='alias')
        ao.remove(ilo)
        self.assertEqual(testvars.alias_one_rm, ao.actions)
    def test_add_multiple(self):
        client = Mock()
        client.indices.get_settings.return_value = testvars.settings_two
        client.cluster.state.return_value = testvars.clu_state_two
        client.indices.stats.return_value = testvars.stats_two
        ilo = curator.IndexList(client)
        ao = curator.Alias(alias='alias')
        ao.add(ilo)
        cmp = sorted(ao.actions, key=lambda k: k['add']['index'])
        self.assertEqual(testvars.alias_two_add, cmp)
    def test_remove_multiple(self):
        client = Mock()
        client.indices.get_settings.return_value = testvars.settings_two
        client.cluster.state.return_value = testvars.clu_state_two
        client.indices.stats.return_value = testvars.stats_two
        ilo = curator.IndexList(client)
        ao = curator.Alias(alias='alias')
        ao.remove(ilo)
        cmp = sorted(ao.actions, key=lambda k: k['remove']['index'])
        self.assertEqual(testvars.alias_two_rm, cmp)
    def test_show_body(self):
        client = Mock()
        client.indices.get_settings.return_value = testvars.settings_one
        client.cluster.state.return_value = testvars.clu_state_one
        client.indices.stats.return_value = testvars.stats_one
        ilo = curator.IndexList(client)
        ao = curator.Alias(alias='alias')
        ao.remove(ilo)
        ao.add(ilo)
        body = ao.body()
        self.assertEqual(
            testvars.alias_one_body['actions'][0], body['actions'][0])
        self.assertEqual(
            testvars.alias_one_body['actions'][1], body['actions'][1])
    def test_raise_on_empty_body(self):
        client = Mock()
        client.indices.get_settings.return_value = testvars.settings_one
        client.cluster.state.return_value = testvars.clu_state_one
        client.indices.stats.return_value = testvars.stats_one
        ilo = curator.IndexList(client)
        ao = curator.Alias(alias='alias')
        self.assertRaises(curator.ActionError, ao.body)
    def test_do_dry_run(self):
        client = Mock()
        client.indices.get_settings.return_value = testvars.settings_one
        client.cluster.state.return_value = testvars.clu_state_one
        client.indices.stats.return_value = testvars.stats_one
        client.indices.update_aliases.return_value = testvars.alias_success
        ilo = curator.IndexList(client)
        ao = curator.Alias(alias='alias')
        ao.add(ilo)
        self.assertIsNone(ao.do_dry_run())
    def test_do_action(self):
        client = Mock()
        client.indices.get_settings.return_value = testvars.settings_one
        client.cluster.state.return_value = testvars.clu_state_one
        client.indices.stats.return_value = testvars.stats_one
        client.indices.update_aliases.return_value = testvars.alias_success
        ilo = curator.IndexList(client)
        ao = curator.Alias(alias='alias')
        ao.add(ilo)
        self.assertIsNone(ao.do_action())
    def test_do_action_raises_exception(self):
        client = Mock()
        client.indices.get_settings.return_value = testvars.settings_one
        client.cluster.state.return_value = testvars.clu_state_one
        client.indices.stats.return_value = testvars.stats_one
        client.indices.update_aliases.return_value = testvars.alias_success
        client.indices.update_aliases.side_effect = testvars.four_oh_one
        ilo = curator.IndexList(client)
        ao = curator.Alias(alias='alias')
        ao.add(ilo)
        self.assertRaises(curator.FailedExecution, ao.do_action)
