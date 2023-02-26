#!/usr/bin/env python

from collections import defaultdict
from dateutil.parser import parse

class Project:
    def __init__(self, name: str) -> None:
        self.name = name
        self._project = {'Milestones': defaultdict(int), 'Components': defaultdict(int), 'Labels': defaultdict(int), 'Issues': []}

    def get_milestones(self) -> dict:
        return self._project['Milestones']
    
    def get_components(self) -> dict:
        return self._project['Components']

    def get_issues(self) -> dict:
        return self._project['Issues']

    def add_item(self, item: object) -> None:
        item_project = self._projectFor(item)
        if item_project != self.name:
            print(f'Skipping item {item.key.text} for project {item_project} current project: {self.name}')
            return

        self._append_item_to_project(item)
    
    def _projectFor(self, item: object) -> str:
        try:
            result = item.project.get('key')
        except AttributeError:
            result = item.key.text.split('-')[0]
        return result

    def _append_item_to_project(self, item: object) -> None:
        closed = str(item.status.get('id')) in ('5', '6')
        closed_at = ''
        if closed:
            try:
                closed_at = self._convert_to_iso(item.resolved.text)
            except AttributeError:
                pass

        self._project['Issues'].append({
            'title': item.title.text,
            'body': self._get_description_text(item),
            'key': item.key.text,
            'created_at': self._convert_to_iso(item.created.text),
            'closed_at': closed_at,
            'updated_at': self._convert_to_iso(item.updated.text),
            'labels': [],
            'comments': [],
            'duplicates': [],
            'is-duplicated-by': [],
            'is-related-to': [],
            'depends-on': [],
            'blocks': []
        })
        if not self._project['Issues'][-1]['closed_at']:
            del self._project['Issues'][-1]['closed_at']

    def  _convert_to_iso(self, timestamp: str):
        dt = parse(timestamp)
        return dt.isoformat()
    
    def _get_description_text(self, item: object) -> str:
        if hasattr(item.description, "p") and item.description.p.text != None:
            return item.description.p.text
        else:
            return ''
