"""
Author: Gary Foreman
Last Modified: November 29, 2014
Sanitizes the WHERE clause entered in the on the Query page.
"""

import re

SQL_KEYWORDS = ['ALTER', 'CREATE', 'DROP', 'DELETE', 'INSERT', 'UPDATE']

def sanitize_where(where_clause):
    malicious_query = False

    for keyword in SQL_KEYWORDS:
        if re.search(keyword, where_clause, flags=re.IGNORECASE):
            malicious_query = True

    return malicious_query
