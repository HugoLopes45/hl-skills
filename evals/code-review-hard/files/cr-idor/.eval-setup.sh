set -e
printf '.claude/\n__pycache__/\n.pytest_cache/\n.eval-setup.sh\n' >> .git/info/exclude
n=0
commit() {
  n=$((n + 1))
  d=$(printf '2024-05-%02dT10:00:00+0000' "$n")
  git add -A
  GIT_AUTHOR_DATE=$d GIT_COMMITTER_DATE=$d git -c user.name=Dev -c user.email=dev@example.com commit -qm "$1"
}
cat > documents.py <<'EOF'
class Forbidden(Exception):
    pass


DOCS = {}


def require_owner(user, doc):
    if doc["owner_id"] != user["id"] and not user.get("is_admin"):
        raise Forbidden(doc["id"])


def get_document(user, doc_id):
    doc = DOCS[doc_id]
    require_owner(user, doc)
    return doc
EOF
cat > routes.py <<'EOF'
from documents import get_document

ROUTES = {
    "GET /documents/<id>": get_document,
}
EOF
commit "feat: documents"
git checkout -qb feature
cat > documents.py <<'EOF'
import csv
import io


class Forbidden(Exception):
    pass


DOCS = {}


def require_owner(user, doc):
    if doc["owner_id"] != user["id"] and not user.get("is_admin"):
        raise Forbidden(doc["id"])


def get_document(user, doc_id):
    doc = DOCS[doc_id]
    require_owner(user, doc)
    return doc


def export_document(user, doc_id):
    """CSV export of a document's rows."""
    doc = DOCS[doc_id]
    out = io.StringIO()
    csv.writer(out).writerows(doc["rows"])
    return out.getvalue()
EOF
cat > routes.py <<'EOF'
from documents import export_document, get_document

ROUTES = {
    "GET /documents/<id>": get_document,
    "GET /documents/<id>/export.csv": export_document,
}
EOF
commit "feat: CSV export"
git rev-parse HEAD > .git/eval-head
