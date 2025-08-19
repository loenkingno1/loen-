# .github/workflows/daily-cdn.yml
name: Daily FX (no Pages)
on:
  schedule: [{ cron: "0 1 * * *" }]  # UTC01:00 ≈ 北京09:00
jobs:
  run:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.11" }
      - run: pip install akshare
      - run: python gen_html.py          # 生成/覆盖 index.html（来源：百度股市通）
      - name: Commit & Push
        run: |
          git config user.name "github-actions"
          git config user.email "actions@github.com"
          git add index.html
          git commit -m "auto: update index.html" || echo "no changes"
          git push
      - name: Purge jsDelivr cache
        run: |
          curl -s "https://purge.jsdelivr.net/gh/<你的GitHub用户名>/<仓库名>@main/index.html"
