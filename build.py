import csv, json, os

nodes = []
with open('/Users/mac/Desktop/光田行銷年度節點/光田行銷年度節點_2026.csv', encoding='utf-8-sig') as f:
    for row in csv.DictReader(f):
        nodes.append({
            'id': row['節點ID'],
            'date': row['日期'],
            'name': row['節點名稱'],
            'date_type': row['日期類型'],
            'cat': row['主類別'],
            'cat_sub': row['副類別'],
            'imp': int(row['重要級']),
            'lead': int(row['提前天數']),
            'dept': row['適用科別'],
            'directions': row['內容方向建議'],
            'p': row['需企劃'],
            'd': row['需美編'],
            'm': row['需多媒體'],
            'pr': row['需公關'],
            'tasks': row['跨組任務模板'],
            'groups': row['預設通知群組'],
            'notes': row['備註'],
            'month': int(row['月份'])
        })

nodes_json = json.dumps(nodes, ensure_ascii=False)
out = os.path.join(os.path.dirname(__file__), 'index.html')
print(f"Building {out} with {len(nodes)} nodes...")

html = f'''<!DOCTYPE html>
<html lang="zh-TW">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>行銷日曆 2026｜光田綜合醫院</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Noto+Sans+TC:wght@400;500;700&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --brand:#006341;--brand-light:#007D53;--brand-bg:#EAF5EE;--brand-bd:#B3D9C5;
  --ci-green:#6EC300;--ci-blue:#00AAC8;--bg:#F3F9F6;--border:#DDE8E3;
  --text:#1A2820;--text-sub:#5A7A6A;--text-muted:#90A89E;
  --sidebar-w:232px;
}}
body{{font-family:'Noto Sans TC',sans-serif;background:var(--bg);color:var(--text);display:flex;min-height:100vh;font-size:14px}}

/* ── Sidebar ── */
.sidebar{{width:var(--sidebar-w);background:var(--brand);position:fixed;top:0;left:0;bottom:0;display:flex;flex-direction:column;z-index:100;overflow-y:auto}}
.sb-logo{{padding:20px 20px 16px;border-bottom:1px solid rgba(255,255,255,.1)}}
.sb-logo .title{{color:#fff;font-size:15px;font-weight:700;line-height:1.3}}
.sb-logo .sub{{color:rgba(255,255,255,.5);font-size:11px;margin-top:2px;font-family:'Inter',sans-serif}}
.sb-logo .dot{{display:inline-block;width:7px;height:7px;background:var(--ci-green);border-radius:50%;margin-right:6px;vertical-align:middle}}
nav{{flex:1;padding:10px 0}}
.nav-group{{margin-bottom:4px}}
.nav-label{{font-size:10px;color:rgba(255,255,255,.35);padding:12px 20px 4px;letter-spacing:.08em;font-weight:600;text-transform:uppercase}}
.nav-item{{display:flex;align-items:center;gap:10px;padding:9px 20px;color:rgba(255,255,255,.75);cursor:pointer;border-left:3px solid transparent;transition:all .15s;font-size:13.5px;text-decoration:none}}
.nav-item:hover{{background:rgba(255,255,255,.07);color:#fff}}
.nav-item.active{{background:rgba(110,195,0,.2);color:#fff;font-weight:600;border-left-color:var(--ci-green)}}
.nav-item svg{{flex-shrink:0;opacity:.8}}
.nav-item.active svg{{opacity:1}}
.sb-footer{{padding:12px 20px;border-top:1px solid rgba(255,255,255,.1);color:rgba(255,255,255,.3);font-size:11px;font-family:'Inter',sans-serif}}

/* ── Main ── */
.main{{margin-left:var(--sidebar-w);flex:1;min-height:100vh}}
.page{{display:none;padding:28px 32px;min-height:100vh}}
.page.active{{display:block}}
.page-title{{font-size:20px;font-weight:700;color:var(--text);margin-bottom:6px;display:flex;align-items:center;gap:10px}}
.page-sub{{color:var(--text-sub);font-size:13px;margin-bottom:24px}}

/* ── Cards ── */
.card{{background:#fff;border:1px solid var(--border);border-radius:12px;padding:20px 24px;box-shadow:0 1px 4px rgba(0,0,0,.05)}}
.card-header{{display:flex;align-items:center;gap:8px;margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid var(--border)}}
.card-title{{font-size:14px;font-weight:600;flex:1}}

/* ── Grid ── */
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:16px}}
.grid-3{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}

/* ── 指揮中心 ── */
.today-banner{{background:linear-gradient(135deg,var(--brand),var(--brand-light));border-radius:14px;padding:22px 28px;color:#fff;margin-bottom:24px;display:flex;align-items:center;justify-content:space-between}}
.today-banner .date-text{{font-size:28px;font-weight:700;font-family:'Inter',sans-serif}}
.today-banner .date-label{{font-size:13px;opacity:.7;margin-top:2px}}
.today-banner .alerts{{display:flex;flex-direction:column;gap:6px;text-align:right}}
.today-banner .alert-chip{{background:rgba(255,255,255,.18);border-radius:20px;padding:4px 12px;font-size:12px;font-weight:500}}

/* Tool cards */
.tool-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:24px}}
.tool-card{{background:#fff;border:1px solid var(--border);border-radius:12px;padding:18px 20px;cursor:pointer;transition:all .2s;text-decoration:none;display:flex;flex-direction:column;gap:8px}}
.tool-card:hover{{border-color:var(--brand-bd);box-shadow:0 4px 12px rgba(0,99,65,.1);transform:translateY(-1px)}}
.tool-card .t-icon{{width:40px;height:40px;border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px}}
.tool-card .t-name{{font-size:14px;font-weight:600;color:var(--text)}}
.tool-card .t-desc{{font-size:12px;color:var(--text-muted);line-height:1.4}}
.tool-card .t-tag{{font-size:11px;color:var(--brand);background:var(--brand-bg);border-radius:12px;padding:2px 8px;align-self:flex-start}}

/* ── 倒數卡片牆 ── */
.countdown-filters{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:20px}}
.filter-btn{{padding:6px 14px;border-radius:20px;border:1px solid var(--border);background:#fff;color:var(--text-sub);font-size:12px;cursor:pointer;font-family:inherit;transition:all .15s}}
.filter-btn.active,.filter-btn:hover{{background:var(--brand);color:#fff;border-color:var(--brand)}}
.countdown-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}}
.node-card{{background:#fff;border:1px solid var(--border);border-radius:12px;padding:16px 18px;transition:box-shadow .15s;cursor:pointer}}
.node-card:hover{{box-shadow:0 4px 16px rgba(0,0,0,.08)}}
.node-card .nc-top{{display:flex;align-items:flex-start;justify-content:space-between;margin-bottom:10px;gap:8px}}
.node-card .nc-name{{font-size:14px;font-weight:600;line-height:1.4;flex:1}}
.node-card .nc-imp{{display:flex;gap:1px;flex-shrink:0}}
.countdown-days{{font-size:32px;font-weight:700;font-family:'Inter',sans-serif;line-height:1}}
.countdown-label{{font-size:11px;color:var(--text-muted);margin-top:2px}}
.node-card .nc-meta{{display:flex;gap:6px;flex-wrap:wrap;margin-top:10px}}
.chip{{font-size:11px;padding:2px 8px;border-radius:10px;border:1px solid var(--border);color:var(--text-sub);background:#fafafa}}
.chip.cat{{color:var(--brand);border-color:var(--brand-bd);background:var(--brand-bg)}}
.chip.urgent{{color:#b91c1c;border-color:#fca5a5;background:#fff1f2}}
.chip.dept{{color:var(--text-muted);}}
.team-dots{{display:flex;gap:4px;margin-top:8px}}
.team-dot{{width:20px;height:20px;border-radius:50%;font-size:9px;font-weight:700;display:flex;align-items:center;justify-content:center;color:#fff}}
.dot-p{{background:#006341}}.dot-d{{background:#6EC300}}.dot-m{{background:#00AAC8}}.dot-pr{{background:#AA7D5F}}

/* Importance stars */
.imp-star{{color:#f59e0b;font-size:12px}}
.nc-card-bar{{height:3px;border-radius:0 0 0 0;margin:-16px -18px 14px;border-radius:10px 10px 0 0}}

/* ── 月曆視圖 ── */
.cal-nav{{display:flex;align-items:center;gap:16px;margin-bottom:20px}}
.cal-nav h2{{font-size:18px;font-weight:700;flex:1}}
.btn{{padding:7px 16px;border-radius:8px;border:1px solid var(--border);background:#fff;color:var(--text);cursor:pointer;font-size:13px;font-family:inherit;transition:all .15s;display:inline-flex;align-items:center;gap:6px}}
.btn:hover{{background:var(--bg)}}
.btn-primary{{background:var(--brand);color:#fff;border-color:var(--brand)}}
.btn-primary:hover{{background:var(--brand-light)}}
.cal-grid{{background:#fff;border:1px solid var(--border);border-radius:12px;overflow:hidden}}
.cal-weekdays{{display:grid;grid-template-columns:repeat(7,1fr);background:var(--brand);color:#fff;font-size:12px;font-weight:600;text-align:center;padding:8px 0}}
.cal-days{{display:grid;grid-template-columns:repeat(7,1fr)}}
.cal-day{{border-right:1px solid var(--border);border-bottom:1px solid var(--border);min-height:90px;padding:6px;position:relative}}
.cal-day:nth-child(7n){{border-right:none}}
.cal-day.other-month .day-num{{color:var(--text-muted);opacity:.4}}
.cal-day.today{{background:var(--brand-bg)}}
.day-num{{font-size:12px;font-weight:600;margin-bottom:4px;font-family:'Inter',sans-serif}}
.cal-day.today .day-num{{color:var(--brand);font-size:14px}}
.cal-node{{font-size:11px;margin-bottom:2px;padding:2px 5px;border-radius:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;cursor:pointer}}
.cal-node.imp-5{{background:#fee2e2;color:#991b1b}}
.cal-node.imp-4{{background:#fef3c7;color:#92400e}}
.cal-node.imp-3{{background:#dbeafe;color:#1e40af}}
.cal-node.imp-2{{background:var(--brand-bg);color:var(--brand)}}
.cal-node.imp-1{{background:#f1f5f9;color:#64748b}}
.cal-more{{font-size:10px;color:var(--text-muted);padding:2px 5px;cursor:pointer}}
.cal-legend{{display:flex;gap:16px;margin-top:16px;flex-wrap:wrap}}
.legend-item{{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--text-sub)}}
.legend-dot{{width:10px;height:10px;border-radius:3px}}

/* ── 清單視圖 ── */
.list-toolbar{{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap;align-items:center}}
.search-box{{flex:1;min-width:200px;padding:8px 14px;border:1px solid var(--border);border-radius:8px;font-size:13px;font-family:inherit;outline:none}}
.search-box:focus{{border-color:var(--brand-bd)}}
select.filter-sel{{padding:8px 12px;border:1px solid var(--border);border-radius:8px;font-size:13px;font-family:inherit;background:#fff;outline:none;color:var(--text);cursor:pointer}}
.list-table-wrap{{background:#fff;border:1px solid var(--border);border-radius:12px;overflow:auto}}
table{{width:100%;border-collapse:collapse}}
thead th{{background:var(--brand);color:#fff;font-size:12px;font-weight:600;padding:10px 12px;text-align:left;white-space:nowrap;position:sticky;top:0}}
tbody tr{{border-bottom:1px solid var(--border);transition:background .1s}}
tbody tr:hover{{background:var(--brand-bg)}}
tbody td{{padding:10px 12px;font-size:13px;vertical-align:top}}
.imp-badge{{display:inline-flex;padding:2px 8px;border-radius:10px;font-size:11px;font-weight:600;white-space:nowrap}}
.imp-5-b{{background:#fee2e2;color:#991b1b}}
.imp-4-b{{background:#fef3c7;color:#92400e}}
.imp-3-b{{background:#dbeafe;color:#1e40af}}
.imp-2-b{{background:var(--brand-bg);color:var(--brand)}}
.imp-1-b{{background:#f1f5f9;color:#64748b}}
.yn-dot{{display:inline-block;width:8px;height:8px;border-radius:50%;margin:0 2px}}
.yn-y{{background:var(--brand)}}.yn-n{{background:#e2e8f0}}
.list-count{{font-size:12px;color:var(--text-muted);margin-left:auto}}

/* ── 年度甘特 ── */
.gantt-wrap{{overflow-x:auto}}
.gantt{{min-width:900px}}
.gantt-header{{display:grid;grid-template-columns:180px repeat(12,1fr);background:var(--brand);color:#fff;border-radius:10px 10px 0 0;overflow:hidden}}
.gantt-header div{{padding:8px 6px;font-size:12px;font-weight:600;text-align:center;border-right:1px solid rgba(255,255,255,.15)}}
.gantt-row{{display:grid;grid-template-columns:180px repeat(12,1fr);border-bottom:1px solid var(--border);background:#fff}}
.gantt-row:nth-child(even){{background:#fafafa}}
.gantt-cat{{padding:10px 12px;font-size:12px;font-weight:600;color:var(--text);border-right:1px solid var(--border)}}
.gantt-cell{{border-right:1px solid var(--border);padding:4px 3px;position:relative;min-height:36px;cursor:default}}
.gantt-pip{{height:20px;border-radius:4px;margin:2px;font-size:9px;color:#fff;display:flex;align-items:center;padding:0 4px;overflow:hidden;white-space:nowrap;cursor:pointer;transition:opacity .15s}}
.gantt-pip:hover{{opacity:.8}}

/* ── Modal ── */
.modal-overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:200;align-items:center;justify-content:center}}
.modal-overlay.open{{display:flex}}
.modal{{background:#fff;border-radius:16px;width:560px;max-width:90vw;max-height:85vh;overflow-y:auto;padding:28px;position:relative}}
.modal-close{{position:absolute;top:16px;right:16px;background:none;border:none;cursor:pointer;color:var(--text-muted);font-size:20px;line-height:1}}
.modal-title{{font-size:18px;font-weight:700;margin-bottom:4px}}
.modal-date{{font-size:13px;color:var(--text-sub);margin-bottom:16px}}
.modal-section{{margin-bottom:14px}}
.modal-section h4{{font-size:12px;font-weight:600;color:var(--text-muted);text-transform:uppercase;letter-spacing:.06em;margin-bottom:6px}}
.modal-section p{{font-size:13px;line-height:1.6;color:var(--text)}}
.task-chain{{display:flex;flex-direction:column;gap:6px}}
.task-item{{display:flex;gap:10px;align-items:flex-start;font-size:12px}}
.task-t{{font-weight:700;color:var(--brand);font-family:'Inter',sans-serif;min-width:36px}}
.team-pills{{display:flex;gap:6px;flex-wrap:wrap;margin-top:6px}}
.team-pill{{padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600;color:#fff}}
.pill-p{{background:#006341}}.pill-d{{background:#6EC300}}.pill-m{{background:#00AAC8}}.pill-pr{{background:#AA7D5F}}

/* ── Responsive ── */
@media(max-width:1100px){{.tool-grid{{grid-template-columns:repeat(2,1fr)}}}}
@media(max-width:800px){{
  .sidebar{{width:60px}}.sidebar .nav-item span,.sidebar .sb-logo .title,.sidebar .sb-logo .sub,.sidebar .nav-label,.sidebar .sb-footer{{display:none}}
  .main{{margin-left:60px}}.tool-grid{{grid-template-columns:1fr}}
}}

/* ── Mark system ── */
.mark-btn{{padding:4px 10px;border-radius:8px;border:1px solid var(--border);font-size:11px;cursor:pointer;font-family:inherit;background:#fff;color:var(--text-sub)}}
.mark-btn.marked{{background:#dcfce7;color:#166534;border-color:#86efac}}
.mark-btn.skip{{background:#fef3c7;color:#92400e;border-color:#fcd34d}}
</style>
</head>
<body>

<!-- ══ SIDEBAR ══════════════════════════════════════════════ -->
<aside class="sidebar">
  <div class="sb-logo">
    <div class="title"><span class="dot"></span>行銷日曆 2026</div>
    <div class="sub">光田綜合醫院 行銷企劃處</div>
  </div>
  <nav>
    <div class="nav-group">
      <div class="nav-label">指揮中心</div>
      <a class="nav-item active" onclick="showPage('home')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
        <span>指揮中心</span>
      </a>
      <a class="nav-item" onclick="showPage('countdown')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        <span>倒數卡片牆</span>
      </a>
    </div>
    <div class="nav-group">
      <div class="nav-label">行事曆</div>
      <a class="nav-item" onclick="showPage('calendar')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
        <span>月曆視圖</span>
      </a>
      <a class="nav-item" onclick="showPage('list')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
        <span>清單視圖</span>
      </a>
      <a class="nav-item" onclick="showPage('gantt')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="16" y2="12"/><line x1="8" y1="18" x2="12" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
        <span>年度甘特</span>
      </a>
    </div>
  </nav>
  <div class="sb-footer">v1.0 · 2026 · 158 節點</div>
</aside>

<!-- ══ MAIN ══════════════════════════════════════════════════ -->
<main class="main">

<!-- ── 指揮中心 ──────────────────────────────────────────── -->
<section class="page active" id="page-home">
  <div id="today-banner"></div>

  <div class="card-header" style="margin-bottom:12px">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--brand)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2"/><line x1="8" y1="21" x2="16" y2="21"/><line x1="12" y1="17" x2="12" y2="21"/></svg>
    <span style="font-size:14px;font-weight:600;color:var(--text)">工具快速入口</span>
  </div>
  <div class="tool-grid" id="tool-grid"></div>

  <div class="grid-2" style="gap:20px">
    <div>
      <div class="card-header" style="margin-bottom:12px">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="var(--brand)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
        <span style="font-size:14px;font-weight:600">本週即將到來</span>
      </div>
      <div id="home-week"></div>
    </div>
    <div>
      <div class="card-header" style="margin-bottom:12px">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#e57373" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
        <span style="font-size:14px;font-weight:600">需提前準備（T-開始）</span>
      </div>
      <div id="home-lead"></div>
    </div>
  </div>
</section>

<!-- ── 倒數卡片牆 ──────────────────────────────────────────── -->
<section class="page" id="page-countdown">
  <div class="page-title">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
    倒數卡片牆
  </div>
  <div class="page-sub">未來 90 天的重點節點，越近越優先</div>
  <div class="countdown-filters" id="cd-filters">
    <button class="filter-btn active" onclick="filterCountdown('all',this)">全部</button>
    <button class="filter-btn" onclick="filterCountdown('5',this)">★★★★★</button>
    <button class="filter-btn" onclick="filterCountdown('4',this)">★★★★</button>
    <button class="filter-btn" onclick="filterCountdown('3',this)">★★★</button>
    <button class="filter-btn" onclick="filterCountdown('p',this)">需企劃</button>
    <button class="filter-btn" onclick="filterCountdown('d',this)">需美編</button>
    <button class="filter-btn" onclick="filterCountdown('m',this)">需多媒體</button>
    <button class="filter-btn" onclick="filterCountdown('pr',this)">需公關</button>
  </div>
  <div class="countdown-grid" id="countdown-grid"></div>
</section>

<!-- ── 月曆視圖 ──────────────────────────────────────────── -->
<section class="page" id="page-calendar">
  <div class="cal-nav">
    <div class="page-title" style="margin-bottom:0">
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
      月曆視圖
    </div>
    <button class="btn" onclick="calMove(-1)">◀ 上個月</button>
    <h2 id="cal-title" style="font-size:17px;font-weight:700;min-width:90px;text-align:center"></h2>
    <button class="btn" onclick="calMove(1)">下個月 ▶</button>
    <button class="btn btn-primary" onclick="calGoToday()">今天</button>
  </div>
  <div class="cal-grid">
    <div class="cal-weekdays">
      <div>日</div><div>一</div><div>二</div><div>三</div><div>四</div><div>五</div><div>六</div>
    </div>
    <div class="cal-days" id="cal-days"></div>
  </div>
  <div class="cal-legend">
    <span class="legend-item"><span class="legend-dot" style="background:#fee2e2"></span>★★★★★ 旗艦</span>
    <span class="legend-item"><span class="legend-dot" style="background:#fef3c7"></span>★★★★ 重要</span>
    <span class="legend-item"><span class="legend-dot" style="background:#dbeafe"></span>★★★ 一般</span>
    <span class="legend-item"><span class="legend-dot" style="background:var(--brand-bg)"></span>★★ 輕量</span>
    <span class="legend-item"><span class="legend-dot" style="background:#f1f5f9"></span>★ 可選</span>
  </div>
</section>

<!-- ── 清單視圖 ──────────────────────────────────────────── -->
<section class="page" id="page-list">
  <div class="page-title">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
    清單視圖
  </div>
  <div class="list-toolbar">
    <input class="search-box" id="list-search" placeholder="搜尋節點名稱、科別..." oninput="renderList()">
    <select class="filter-sel" id="f-month" onchange="renderList()"><option value="">全年月份</option></select>
    <select class="filter-sel" id="f-cat" onchange="renderList()"><option value="">全部類別</option></select>
    <select class="filter-sel" id="f-imp" onchange="renderList()"><option value="">全部重要級</option></select>
    <select class="filter-sel" id="f-team" onchange="renderList()">
      <option value="">全組</option>
      <option value="p">需企劃</option>
      <option value="d">需美編</option>
      <option value="m">需多媒體</option>
      <option value="pr">需公關</option>
    </select>
    <span class="list-count" id="list-count"></span>
  </div>
  <div class="list-table-wrap">
    <table>
      <thead>
        <tr>
          <th>日期</th><th>節點名稱</th><th>主類別</th><th>重要級</th>
          <th>適用科別</th><th>跨組</th><th>提前天數</th><th>標記</th>
        </tr>
      </thead>
      <tbody id="list-body"></tbody>
    </table>
  </div>
</section>

<!-- ── 年度甘特 ──────────────────────────────────────────── -->
<section class="page" id="page-gantt">
  <div class="page-title">
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="16" y2="12"/><line x1="8" y1="18" x2="12" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>
    年度甘特
  </div>
  <div class="page-sub">各類別節點在 2026 年的分佈（數字=節點數，點擊看詳情）</div>
  <div class="gantt-wrap" id="gantt-wrap"></div>
</section>

</main>

<!-- ══ MODAL ════════════════════════════════════════════════ -->
<div class="modal-overlay" id="modal" onclick="if(event.target===this)closeModal()">
  <div class="modal" id="modal-body"></div>
</div>

<!-- ══ SCRIPT ════════════════════════════════════════════════ -->
<script>
const NODES = {nodes_json};

// ── 6 Tools ──────────────────────────────────────────────────
const TOOLS = [
  {{name:'行銷整合分析中心',desc:'FB/GA4/媒體/活動跨平台成效分析',tag:'數據分析',icon:'📊',color:'#006341',url:'https://kyoape-ux.github.io/ktgh-marketing-hub/'}},
  {{name:'美編小助手',desc:'海報、貼文素材快速產出與管理',tag:'美編輔助',icon:'🎨',color:'#6EC300',url:'https://kyoape-ux.github.io/kuangtien-poster-generator/'}},
  {{name:'工作進度控管',desc:'跨組任務追蹤、截止日提醒',tag:'專案管理',icon:'📋',color:'#00AAC8',url:'https://kyoape-ux.github.io/kuangtien-pm/'}},
  {{name:'影音小助手',desc:'影片素材整理、字幕、版本管理',tag:'多媒體',icon:'🎬',color:'#AA7D5F',url:'#'}},
  {{name:'影片發布管理',desc:'YouTube 發布資訊紀錄與查詢',tag:'發布追蹤',icon:'▶',color:'#C0313D',url:'#'}},
  {{name:'視覺多媒體工具站',desc:'設計工具整合入口與素材下載',tag:'設計資源',icon:'🖥',color:'#14286E',url:'https://kyoape-ux.github.io/'}},
];

// ── Helpers ──────────────────────────────────────────────────
const today = new Date(); today.setHours(0,0,0,0);
const todayStr = `${{today.getFullYear()}}/${{String(today.getMonth()+1).padStart(2,'0')}}/${{String(today.getDate()).padStart(2,'0')}}`;

function parseDate(s){{ const[y,m,d]=s.split('/'); return new Date(+y,+m-1,+d); }}
function daysUntil(dateStr){{ return Math.round((parseDate(dateStr)-today)/86400000); }}
function stars(n){{ return '★'.repeat(n)+'☆'.repeat(5-n); }}
function impClass(n){{ return ['','imp-1','imp-2','imp-3','imp-4','imp-5'][n]; }}
function impBadge(n){{ const cls=['','imp-1-b','imp-2-b','imp-3-b','imp-4-b','imp-5-b'][n]; return `<span class="imp-badge ${{cls}}">${{'★'.repeat(n)}}</span>`; }}
function impColor(n){{ return ['#f1f5f9','#EAF5EE','#dbeafe','#fef3c7','#fee2e2'][n-1]||'#f1f5f9'; }}
function impDark(n){{ return ['#64748b','#006341','#1e40af','#92400e','#991b1b'][n-1]||'#64748b'; }}
function catColor(c){{
  const m={{'醫療專業日':'#00AAC8','主題月':'#6EC300','國定/民俗節慶':'#FFB900','台灣醫療節':'#006341','政府衛福政策':'#14286E','季節性醫療議題':'#AA7D5F','院內節點':'#C0313D','在地節慶':'#e67e22'}};
  return m[c]||'#888';
}}
const MARKS = JSON.parse(localStorage.getItem('ktgh_cal_marks_v1')||'{{}}');
function saveMark(id,v){{ if(v==='none') delete MARKS[id]; else MARKS[id]=v; localStorage.setItem('ktgh_cal_marks_v1',JSON.stringify(MARKS)); }}

// ── Page routing ───────────────────────────────────────────
function showPage(p){{
  document.querySelectorAll('.page').forEach(el=>el.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(el=>el.classList.remove('active'));
  document.getElementById('page-'+p).classList.add('active');
  document.querySelectorAll('.nav-item').forEach(el=>{{
    if(el.getAttribute('onclick')?.includes("'"+p+"'")) el.classList.add('active');
  }});
  if(p==='calendar') renderCalendar();
  if(p==='list') renderList();
  if(p==='countdown') renderCountdown('all');
  if(p==='gantt') renderGantt();
}}

// ── 指揮中心 ─────────────────────────────────────────────────
function renderHome(){{
  // Banner
  const days30 = NODES.filter(n=>{{const d=daysUntil(n.date);return d>=0&&d<=30&&n.imp>=4;}});
  const daysAlert = NODES.filter(n=>{{const d=daysUntil(n.date);return d>=0&&d<=7;}});
  document.getElementById('today-banner').innerHTML=`
    <div class="today-banner">
      <div>
        <div class="date-text">${{today.getFullYear()}} / ${{String(today.getMonth()+1).padStart(2,'0')}} / ${{String(today.getDate()).padStart(2,'0')}}</div>
        <div class="date-label">今日 · 光田行銷企劃處 指揮台</div>
      </div>
      <div class="alerts">
        <div class="alert-chip">未來 30 天重要節點：${{days30.length}} 個</div>
        <div class="alert-chip">本週到期：${{daysAlert.length}} 個</div>
        <div class="alert-chip">全年節點：${{NODES.length}} 個</div>
      </div>
    </div>`;

  // Tools
  document.getElementById('tool-grid').innerHTML = TOOLS.map(t=>`
    <a class="tool-card" href="${{t.url}}" target="_blank" rel="noopener">
      <div class="t-icon" style="background:${{t.color}}22;color:${{t.color}}">${{t.icon}}</div>
      <div class="t-name">${{t.name}}</div>
      <div class="t-desc">${{t.desc}}</div>
      <div class="t-tag">${{t.tag}}</div>
    </a>`).join('');

  // 本週節點
  const week = NODES.filter(n=>{{const d=daysUntil(n.date);return d>=0&&d<=7;}}).slice(0,6);
  document.getElementById('home-week').innerHTML = week.length ?
    week.map(n=>{{
      const d=daysUntil(n.date);
      return `<div class="card" style="margin-bottom:8px;padding:12px 16px;cursor:pointer" onclick="openModal('${{n.id}}')">
        <div style="display:flex;align-items:center;gap:10px">
          <div style="font-size:22px;font-weight:700;color:${{d===0?'#ef4444':'var(--brand)'}};font-family:'Inter',sans-serif;min-width:32px">${{d===0?'今':d}}</div>
          <div>
            <div style="font-size:13px;font-weight:600">${{n.name}}</div>
            <div style="font-size:11px;color:var(--text-muted)">${{n.date}} · ${{n.cat}}</div>
          </div>
          <div style="margin-left:auto">${{impBadge(n.imp)}}</div>
        </div>
      </div>`;
    }}).join('') : '<div class="card" style="color:var(--text-muted);font-size:13px">本週無節點</div>';

  // 需提前準備
  const leads = NODES.filter(n=>{{
    const d=daysUntil(n.date);
    return d>0&&d<=n.lead&&n.imp>=4;
  }}).sort((a,b)=>daysUntil(a.date)-daysUntil(b.date)).slice(0,6);
  document.getElementById('home-lead').innerHTML = leads.length ?
    leads.map(n=>{{
      const d=daysUntil(n.date);
      const prep=d-n.lead;
      return `<div class="card" style="margin-bottom:8px;padding:12px 16px;cursor:pointer" onclick="openModal('${{n.id}}')">
        <div style="display:flex;align-items:center;gap:10px">
          <div style="font-size:12px;font-weight:700;color:#ef4444;font-family:'Inter',sans-serif;min-width:44px">T-${{d}}</div>
          <div>
            <div style="font-size:13px;font-weight:600">${{n.name}}</div>
            <div style="font-size:11px;color:var(--text-muted)">${{n.date}} · 應提前 ${{n.lead}} 天</div>
          </div>
          <div style="margin-left:auto">${{impBadge(n.imp)}}</div>
        </div>
      </div>`;
    }}).join('') : '<div class="card" style="color:var(--text-muted);font-size:13px">無需提前準備的高優先節點</div>';
}}

// ── 倒數卡片牆 ───────────────────────────────────────────────
let cdFilter = 'all';
function filterCountdown(f,btn){{
  cdFilter=f;
  document.querySelectorAll('#cd-filters .filter-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  renderCountdown(f);
}}
function renderCountdown(f){{
  let nodes = NODES.filter(n=>{{const d=daysUntil(n.date);return d>=0&&d<=90;}});
  if(f==='5') nodes=nodes.filter(n=>n.imp===5);
  else if(f==='4') nodes=nodes.filter(n=>n.imp===4);
  else if(f==='3') nodes=nodes.filter(n=>n.imp===3);
  else if(f==='p') nodes=nodes.filter(n=>n.p==='Y');
  else if(f==='d') nodes=nodes.filter(n=>n.d==='Y');
  else if(f==='m') nodes=nodes.filter(n=>n.m==='Y');
  else if(f==='pr') nodes=nodes.filter(n=>n.pr==='Y');
  nodes.sort((a,b)=>daysUntil(a.date)-daysUntil(b.date));

  const grid=document.getElementById('countdown-grid');
  if(!nodes.length){{grid.innerHTML='<div style="color:var(--text-muted);font-size:14px">未來 90 天無符合條件的節點</div>';return;}}
  grid.innerHTML=nodes.map(n=>{{
    const d=daysUntil(n.date);
    const mark=MARKS[n.id]||'none';
    const teams=[];
    if(n.p==='Y')teams.push('<span class="team-dot dot-p">企</span>');
    if(n.d==='Y')teams.push('<span class="team-dot dot-d">美</span>');
    if(n.m==='Y')teams.push('<span class="team-dot dot-m">媒</span>');
    if(n.pr==='Y')teams.push('<span class="team-dot dot-pr">公</span>');
    return `<div class="node-card" style="border-top:3px solid ${{catColor(n.cat)}}">
      <div class="nc-top">
        <div class="nc-name">${{n.name}}</div>
        <div class="nc-imp"><span style="color:#f59e0b;font-size:14px">${{'★'.repeat(n.imp)}}</span></div>
      </div>
      <div style="display:flex;align-items:flex-end;gap:16px" onclick="openModal('${{n.id}}')">
        <div>
          <div class="countdown-days" style="color:${{d<=7?'#ef4444':d<=14?'#f59e0b':'var(--brand)}}">${{d===0?'今天':d}}</div>
          <div class="countdown-label">${{d===0?'':d===1?'明天':'天後'}}</div>
        </div>
        <div style="flex:1">
          <div style="font-size:11px;color:var(--text-muted)">${{n.date}}</div>
          <div class="nc-meta">
            <span class="chip cat">${{n.cat}}</span>
            ${{d<=n.lead?'<span class="chip urgent">⚡ 應備稿</span>':''}}
          </div>
        </div>
      </div>
      <div style="display:flex;align-items:center;justify-content:space-between;margin-top:10px">
        <div class="team-dots">${{teams.join('')}}</div>
        <div style="display:flex;gap:4px">
          <button class="mark-btn ${{mark==='marked'?'marked':''}}" onclick="toggleMark('${{n.id}}','marked',this)">✓ 確認執行</button>
          <button class="mark-btn ${{mark==='skip'?'skip':''}}" onclick="toggleMark('${{n.id}}','skip',this)">↷ 本次跳過</button>
        </div>
      </div>
    </div>`;
  }}).join('');
}}
function toggleMark(id,val,btn){{
  const cur=MARKS[id]||'none';
  const next=cur===val?'none':val;
  saveMark(id,next);
  // re-render current page
  renderCountdown(cdFilter);
}}

// ── 月曆視圖 ─────────────────────────────────────────────────
let calYear=today.getFullYear(), calMonth=today.getMonth();
function calMove(d){{calMonth+=d;if(calMonth>11){{calMonth=0;calYear++;}}if(calMonth<0){{calMonth=11;calYear--;}}renderCalendar();}}
function calGoToday(){{calYear=today.getFullYear();calMonth=today.getMonth();renderCalendar();}}
function renderCalendar(){{
  const MONTHS=['一月','二月','三月','四月','五月','六月','七月','八月','九月','十月','十一月','十二月'];
  document.getElementById('cal-title').textContent=`${{calYear}} 年 ${{MONTHS[calMonth]}}`;
  const first=new Date(calYear,calMonth,1);
  const last=new Date(calYear,calMonth+1,0);
  const startDow=first.getDay();
  const monthNodes=NODES.filter(n=>{{
    const[y,m]=n.date.split('/').map(Number);
    return y===calYear&&m===calMonth+1;
  }});
  const byDay={{}};
  monthNodes.forEach(n=>{{const d=parseInt(n.date.split('/')[2]);(byDay[d]||(byDay[d]=[])).push(n);}});
  let cells='';
  // prev month days
  const prevLast=new Date(calYear,calMonth,0).getDate();
  for(let i=startDow-1;i>=0;i--){{
    cells+=`<div class="cal-day other-month"><div class="day-num">${{prevLast-i}}</div></div>`;
  }}
  for(let d=1;d<=last.getDate();d++){{
    const isToday=calYear===today.getFullYear()&&calMonth===today.getMonth()&&d===today.getDate();
    const ns=(byDay[d]||[]).sort((a,b)=>b.imp-a.imp);
    const shown=ns.slice(0,3);
    const more=ns.length-shown.length;
    cells+=`<div class="cal-day${{isToday?' today':''}}">
      <div class="day-num">${{d}}</div>
      ${{shown.map(n=>`<div class="cal-node ${{impClass(n.imp)}}" onclick="openModal('${{n.id}}')" title="${{n.name}}">${{n.name}}</div>`).join('')}}
      ${{more>0?`<div class="cal-more">+${{more}} 個</div>`:''}}
    </div>`;
  }}
  // next month
  const total=startDow+last.getDate();
  const remaining=(7-total%7)%7;
  for(let d=1;d<=remaining;d++){{
    cells+=`<div class="cal-day other-month"><div class="day-num">${{d}}</div></div>`;
  }}
  document.getElementById('cal-days').innerHTML=cells;
}}

// ── 清單視圖 ─────────────────────────────────────────────────
function initListFilters(){{
  const fm=document.getElementById('f-month');
  for(let m=1;m<=12;m++) fm.innerHTML+=`<option value="${{m}}">${{m}}月</option>`;
  const cats=[...new Set(NODES.map(n=>n.cat))].sort();
  const fc=document.getElementById('f-cat');
  cats.forEach(c=>fc.innerHTML+=`<option value="${{c}}">${{c}}</option>`);
  const fi=document.getElementById('f-imp');
  [5,4,3,2,1].forEach(i=>fi.innerHTML+=`<option value="${{i}}">${{'★'.repeat(i)}}</option>`);
}}
function renderList(){{
  const q=document.getElementById('list-search').value.toLowerCase();
  const m=+document.getElementById('f-month').value||0;
  const cat=document.getElementById('f-cat').value;
  const imp=+document.getElementById('f-imp').value||0;
  const team=document.getElementById('f-team').value;
  let nodes=NODES.filter(n=>{{
    if(q&&!n.name.toLowerCase().includes(q)&&!n.dept.toLowerCase().includes(q))return false;
    if(m&&n.month!==m)return false;
    if(cat&&n.cat!==cat)return false;
    if(imp&&n.imp!==imp)return false;
    if(team==='p'&&n.p!=='Y')return false;
    if(team==='d'&&n.d!=='Y')return false;
    if(team==='m'&&n.m!=='Y')return false;
    if(team==='pr'&&n.pr!=='Y')return false;
    return true;
  }});
  document.getElementById('list-count').textContent=`共 ${{nodes.length}} 筆`;
  const tbody=document.getElementById('list-body');
  tbody.innerHTML=nodes.map(n=>{{
    const mark=MARKS[n.id]||'none';
    return `<tr>
      <td style="white-space:nowrap;font-family:'Inter',sans-serif;font-size:12px">${{n.date}}</td>
      <td style="font-weight:500;cursor:pointer;max-width:200px" onclick="openModal('${{n.id}}')">${{n.name}}</td>
      <td><span style="font-size:11px;padding:2px 7px;border-radius:8px;background:${{catColor(n.cat)}}22;color:${{catColor(n.cat)}};font-weight:600">${{n.cat}}</span></td>
      <td>${{impBadge(n.imp)}}</td>
      <td style="font-size:12px;color:var(--text-sub);max-width:150px">${{n.dept}}</td>
      <td>
        <span class="yn-dot yn-${{n.p==='Y'?'y':'n'}}" title="企劃"></span>
        <span class="yn-dot yn-${{n.d==='Y'?'y':'n'}}" title="美編"></span>
        <span class="yn-dot yn-${{n.m==='Y'?'y':'n'}}" title="多媒體"></span>
        <span class="yn-dot yn-${{n.pr==='Y'?'y':'n'}}" title="公關"></span>
      </td>
      <td style="text-align:center;font-size:12px;color:var(--text-sub)">${{n.lead}}天</td>
      <td>
        <select onchange="saveMark('${{n.id}}',this.value);renderList()" style="font-size:11px;border:1px solid var(--border);border-radius:6px;padding:2px 4px;background:#fff">
          <option value="none" ${{mark==='none'?'selected':''}}>—</option>
          <option value="marked" ${{mark==='marked'?'selected':''}}>✓ 確認</option>
          <option value="skip" ${{mark==='skip'?'selected':''}}>↷ 跳過</option>
        </select>
      </td>
    </tr>`;
  }}).join('');
}}

// ── 年度甘特 ─────────────────────────────────────────────────
function renderGantt(){{
  const CATS=['醫療專業日','主題月','國定/民俗節慶','台灣醫療節','政府衛福政策','季節性醫療議題','院內節點'];
  const MONTHS=['1月','2月','3月','4月','5月','6月','7月','8月','9月','10月','11月','12月'];
  let html=`<div class="gantt">
    <div class="gantt-header">
      <div style="text-align:left;padding-left:12px">類別</div>
      ${{MONTHS.map(m=>`<div>${{m}}</div>`).join('')}}
    </div>`;
  CATS.forEach(cat=>{{
    html+=`<div class="gantt-row"><div class="gantt-cat">${{cat}}</div>`;
    for(let m=1;m<=12;m++){{
      const ns=NODES.filter(n=>n.cat===cat&&n.month===m).sort((a,b)=>b.imp-a.imp);
      html+=`<div class="gantt-cell">`;
      ns.slice(0,3).forEach(n=>{{
        html+=`<div class="gantt-pip" style="background:${{catColor(cat)}};opacity:${{0.5+n.imp*0.1}}" onclick="openModal('${{n.id}}')" title="${{n.name}}">${{n.name.substring(0,8)}}</div>`;
      }});
      if(ns.length>3) html+=`<div style="font-size:9px;color:var(--text-muted);padding:0 3px">+${{ns.length-3}}</div>`;
      html+='</div>';
    }}
    html+='</div>';
  }});
  html+='</div>';
  document.getElementById('gantt-wrap').innerHTML=html;
}}

// ── Modal ─────────────────────────────────────────────────────
function openModal(id){{
  const n=NODES.find(x=>x.id===id); if(!n) return;
  const d=daysUntil(n.date);
  const tasks=n.tasks.split(' | ').map(t=>{{
    const m=t.match(/^(T-\\d+)\\s(.+)$/);
    return m?`<div class="task-item"><span class="task-t">${{m[1]}}</span><span>${{m[2]}}</span></div>`:t;
  }}).join('');
  const teams=[];
  if(n.p==='Y')teams.push('<span class="team-pill pill-p">企劃</span>');
  if(n.d==='Y')teams.push('<span class="team-pill pill-d">美編</span>');
  if(n.m==='Y')teams.push('<span class="team-pill pill-m">多媒體</span>');
  if(n.pr==='Y')teams.push('<span class="team-pill pill-pr">公關</span>');
  document.getElementById('modal-body').innerHTML=`
    <button class="modal-close" onclick="closeModal()">✕</button>
    <div style="height:4px;background:${{catColor(n.cat)}};border-radius:4px;margin-bottom:16px"></div>
    <div style="font-size:11px;color:${{catColor(n.cat)}};font-weight:600;margin-bottom:4px">${{n.cat}}</div>
    <div class="modal-title">${{n.name}}</div>
    <div class="modal-date">${{n.date}} · ${{d===0?'今天':d>0?`${{d}} 天後`:`${{Math.abs(d)}} 天前`}} · ${{n.date_type}}</div>
    <div style="display:flex;gap:12px;margin-bottom:16px;flex-wrap:wrap">
      ${{impBadge(n.imp)}}
      <span style="font-size:12px;color:var(--text-sub)">需提前 ${{n.lead}} 天</span>
      ${{d<=n.lead&&d>=0?'<span style="color:#ef4444;font-size:12px;font-weight:600">⚡ 現在應開始準備</span>':''}}
    </div>
    ${{teams.length?`<div class="modal-section"><h4>協作組別</h4><div class="team-pills">${{teams.join('')}}</div></div>`:''}}
    <div class="modal-section"><h4>適用科別</h4><p>${{n.dept}}</p></div>
    <div class="modal-section"><h4>內容方向建議</h4><p>${{n.directions}}</p></div>
    <div class="modal-section"><h4>跨組任務鏈</h4><div class="task-chain">${{tasks}}</div></div>
    ${{n.notes?`<div class="modal-section"><h4>備註</h4><p>${{n.notes}}</p></div>`:''}}
    <div class="modal-section"><h4>節點 ID</h4><p style="font-family:'Inter',sans-serif;font-size:12px;color:var(--text-muted)">${{n.id}}</p></div>`;
  document.getElementById('modal').classList.add('open');
}}
function closeModal(){{ document.getElementById('modal').classList.remove('open'); }}
document.addEventListener('keydown',e=>{{if(e.key==='Escape')closeModal();}});

// ── Init ──────────────────────────────────────────────────────
renderHome();
initListFilters();
</script>
</body>
</html>'''

with open(out, 'w', encoding='utf-8') as f:
    f.write(html)
print(f"Done! {out}")
