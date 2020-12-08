""" Notion manager module """
from jira.resources import Issue
from notion.client import NotionClient
from notion.block import PageBlock
from notion.block import TextBlock
from notion.block import HeaderBlock
from notion.block import TodoBlock
from notion.block import BookmarkBlock
from notion.block import SubheaderBlock
from notion.block import DividerBlock
from notion.block import QuoteBlock
from notion.block import CollectionViewBlock
from config import Config
from jira_manager import JiraManager


class NotionManager:
    """ Notion manager class """

    def __init__(self, c: Config):
        self._config = c
        self._client = NotionClient(token_v2=self._config.notion_token_v2)
        self._colection_view = self._client.get_collection_view(
            self._config.notion_page)

    def create_page(self, issue: Issue, jira_man: JiraManager):
        """ Creates a new Notion page """

        try:
            title_key = issue.fields.parent.key
        except Exception:
            title_key = issue.key

        # only remains title number (Remove 'ADSK')
        title = title_key[5:] + " : " + issue.fields.summary

        row = self._colection_view.collection.add_row()
        row.name = title
        assignee = issue.fields.assignee.displayName
        reporter = issue.fields.reporter.displayName
        row.set_property('Assignee', assignee.replace('.', ' '))
        row.set_property('Reporter', reporter.replace('.', ' '))
        row.set_property('Updated by', 'Albert')

        # TODO : switch for others (long term, action for close, etc..)
        status = issue.fields.customfield_10010.currentStatus.status
        # status.replace('Waiting', 'w')
        # if (status == 'Waiting for support') {
        #     status = 'w for support'
        # } else if (status == 'Waiting for customer') {
        #     status = 'w for customer'
        # }
        row.set_property('Status', status.replace('Waiting', 'w'))
        row.set_property('Link', issue.fields.customfield_10010._links.agent)