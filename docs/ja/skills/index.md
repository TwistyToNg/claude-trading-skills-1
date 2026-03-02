---
layout: default
title: スキルガイド
parent: 日本語
nav_order: 3
has_children: true
lang_peer: /en/skills/
permalink: /ja/skills/
---

# スキルガイド

各スキルの実践ガイドです。具体的な使用例、ワークフローの解説、活用のコツを含みます。

手動作成ガイド（★マーク）は10セクション構成の詳細ガイドです。自動生成ガイドはSKILL.mdから概要・前提条件・ワークフロー・リソース一覧を抽出したものです。

> 検索は英語スキル名（"CANSLIM", "VCP", "FinViz"等）での検索を推奨します。日本語の部分一致検索は制限があります。
{: .note }

---

## 利用可能なガイド

| スキル | 概要 | API |
|--------|------|-----|
| [Backtest Expert]({{ '/ja/skills/backtest-expert/' | relative_url }}) ★ | バックテスト結果の5次元スコアリング評価 | <span class="badge badge-free">API不要</span> |
| [Breadth Chart Analyst]({{ '/ja/skills/breadth-chart-analyst/' | relative_url }}) | S&P 500 ブレッドチャート分析 | <span class="badge badge-free">API不要</span> |
| [CANSLIM Screener]({{ '/ja/skills/canslim-screener/' | relative_url }}) ★ | O'Neilの7要素CANSLIMグロース株スクリーニング | <span class="badge badge-api">FMP必須</span> |
| [Data Quality Checker]({{ '/ja/skills/data-quality-checker/' | relative_url }}) | 分析ドキュメントのデータ品質検証 | <span class="badge badge-free">API不要</span> |
| [Dividend Growth Pullback Screener]({{ '/ja/skills/dividend-growth-pullback-screener/' | relative_url }}) | RSI押し目で高品質配当成長株を発見 | <span class="badge badge-api">FMP必須</span> <span class="badge badge-optional">FINVIZ任意</span> |
| [Dual Axis Skill Reviewer]({{ '/ja/skills/dual-axis-skill-reviewer/' | relative_url }}) | 2軸スキル品質レビュー | <span class="badge badge-free">API不要</span> |
| [Earnings Calendar]({{ '/ja/skills/earnings-calendar/' | relative_url }}) | FMP APIによる決算発表カレンダー | <span class="badge badge-api">FMP必須</span> |
| [Earnings Trade Analyzer]({{ '/ja/skills/earnings-trade-analyzer/' | relative_url }}) | 決算後5要素スコアリング分析 | <span class="badge badge-api">FMP必須</span> |
| [Economic Calendar Fetcher]({{ '/ja/skills/economic-calendar-fetcher/' | relative_url }}) | 経済イベント・データリリース取得 | <span class="badge badge-api">FMP必須</span> |
| [Edge Candidate Agent]({{ '/ja/skills/edge-candidate-agent/' | relative_url }}) | EOD観測からエッジ研究チケット生成 | <span class="badge badge-free">API不要</span> |
| [Edge Concept Synthesizer]({{ '/ja/skills/edge-concept-synthesizer/' | relative_url }}) | チケットとヒントを再利用可能なエッジ概念に抽象化 | <span class="badge badge-free">API不要</span> |
| [Edge Hint Extractor]({{ '/ja/skills/edge-hint-extractor/' | relative_url }}) | 日次市場観測からエッジヒント抽出 | <span class="badge badge-free">API不要</span> |
| [Edge Pipeline Orchestrator]({{ '/ja/skills/edge-pipeline-orchestrator/' | relative_url }}) | エッジ研究パイプライン全体のオーケストレーション | <span class="badge badge-free">API不要</span> |
| [Edge Strategy Designer]({{ '/ja/skills/edge-strategy-designer/' | relative_url }}) | エッジ概念を戦略ドラフトバリアントに変換 | <span class="badge badge-free">API不要</span> |
| [Edge Strategy Reviewer]({{ '/ja/skills/edge-strategy-reviewer/' | relative_url }}) | 戦略ドラフトのエッジ妥当性・過学習リスクレビュー | <span class="badge badge-free">API不要</span> |
| [FinViz Screener]({{ '/ja/skills/finviz-screener/' | relative_url }}) ★ | 自然言語でFinVizスクリーニングURL構築 | <span class="badge badge-free">API不要</span> <span class="badge badge-optional">FINVIZ任意</span> |
| [FTD Detector]({{ '/ja/skills/ftd-detector/' | relative_url }}) | フォロースルーデイ検出（市場底値確認） | <span class="badge badge-free">API不要</span> |
| [Institutional Flow Tracker]({{ '/ja/skills/institutional-flow-tracker/' | relative_url }}) | 13Fファイリングによる機関投資家フロー追跡 | <span class="badge badge-api">FMP必須</span> |
| [Kanchi Dividend Review Monitor]({{ '/ja/skills/kanchi-dividend-review-monitor/' | relative_url }}) | カンチ式強制レビュートリガー（T1-T5）モニター | <span class="badge badge-free">API不要</span> |
| [Kanchi Dividend SOP]({{ '/ja/skills/kanchi-dividend-sop/' | relative_url }}) | カンチ式配当投資の米国株SOP化 | <span class="badge badge-free">API不要</span> |
| [Kanchi Dividend US Tax Accounting]({{ '/ja/skills/kanchi-dividend-us-tax-accounting/' | relative_url }}) | 米国配当税務・口座配置ワークフロー | <span class="badge badge-free">API不要</span> |
| [Macro Regime Detector]({{ '/ja/skills/macro-regime-detector/' | relative_url }}) | クロスアセット比率によるマクロレジーム転換検出 | <span class="badge badge-free">API不要</span> |
| [Market Breadth Analyzer]({{ '/ja/skills/market-breadth-analyzer/' | relative_url }}) ★ | TraderMontyのCSVデータで市場ブレッド健全性を定量化 | <span class="badge badge-free">API不要</span> |
| [Market Environment Analysis]({{ '/ja/skills/market-environment-analysis/' | relative_url }}) | 包括的市場環境分析・レポーティング | <span class="badge badge-free">API不要</span> |
| [Market News Analyst]({{ '/ja/skills/market-news-analyst/' | relative_url }}) ★ | 最新マーケットニュースの影響度分析 | <span class="badge badge-free">API不要</span> |
| [Market Top Detector]({{ '/ja/skills/market-top-detector/' | relative_url }}) | O'Neilディストリビューションデイ + Minerviniシグナルで天井確率判定 | <span class="badge badge-free">API不要</span> |
| [Options Strategy Advisor]({{ '/ja/skills/options-strategy-advisor/' | relative_url }}) | オプション戦略分析・ブラックショールズシミュレーション | <span class="badge badge-free">API不要</span> <span class="badge badge-optional">FMP任意</span> |
| [Pair Trade Screener]({{ '/ja/skills/pair-trade-screener/' | relative_url }}) | 統計的裁定ペアトレード探索 | <span class="badge badge-api">FMP必須</span> |
| [PEAD Screener]({{ '/ja/skills/pead-screener/' | relative_url }}) | 決算後アナウンスメント・ドリフトパターン検出 | <span class="badge badge-api">FMP必須</span> |
| [Portfolio Manager]({{ '/ja/skills/portfolio-manager/' | relative_url }}) | Alpaca MCP Server連携ポートフォリオ分析 | <span class="badge badge-api">Alpaca必須</span> |
| [Position Sizer]({{ '/ja/skills/position-sizer/' | relative_url }}) ★ | リスクベースポジションサイジング・Kelly Criterion | <span class="badge badge-free">API不要</span> |
| [Scenario Analyzer]({{ '/ja/skills/scenario-analyzer/' | relative_url }}) | ニュースヘッドラインから18ヶ月シナリオ分析 | <span class="badge badge-free">API不要</span> |
| [Sector Analyst]({{ '/ja/skills/sector-analyst/' | relative_url }}) | セクターローテーション分析・市場サイクル判定 | <span class="badge badge-free">API不要</span> |
| [Skill Designer]({{ '/ja/skills/skill-designer/' | relative_url }}) | 構造化されたアイデア仕様から新スキル設計 | <span class="badge badge-free">API不要</span> |
| [Skill Idea Miner]({{ '/ja/skills/skill-idea-miner/' | relative_url }}) | セッションログからスキルアイデア候補を採掘 | <span class="badge badge-free">API不要</span> |
| [Stanley Druckenmiller Investment]({{ '/ja/skills/stanley-druckenmiller-investment/' | relative_url }}) | 8つの上流スキルを統合するDruckenmiller戦略シンセサイザー | <span class="badge badge-free">API不要</span> |
| [Strategy Pivot Designer]({{ '/ja/skills/strategy-pivot-designer/' | relative_url }}) | バックテスト停滞検出と戦略ピボット提案 | <span class="badge badge-free">API不要</span> |
| [Technical Analyst]({{ '/ja/skills/technical-analyst/' | relative_url }}) | 株式・指数・暗号資産の週足チャート分析 | <span class="badge badge-free">API不要</span> |
| [Theme Detector]({{ '/ja/skills/theme-detector/' | relative_url }}) ★ | セクター横断テーマ検出（3Dスコアリング） | <span class="badge badge-free">API不要</span> <span class="badge badge-optional">FMP任意</span> <span class="badge badge-optional">FINVIZ任意</span> |
| [Uptrend Analyzer]({{ '/ja/skills/uptrend-analyzer/' | relative_url }}) | Monty Uptrend Ratioダッシュボードで市場ブレッド診断 | <span class="badge badge-free">API不要</span> |
| [US Market Bubble Detector]({{ '/ja/skills/us-market-bubble-detector/' | relative_url }}) ★ | 改訂版Minsky/Kindlebergerモデルによるバブルリスク定量評価 | <span class="badge badge-free">API不要</span> |
| [US Stock Analysis]({{ '/ja/skills/us-stock-analysis/' | relative_url }}) ★ | 包括的な米国株ファンダメンタル＋テクニカル分析 | <span class="badge badge-free">API不要</span> |
| [Value Dividend Screener]({{ '/ja/skills/value-dividend-screener/' | relative_url }}) | バリュー+インカム基準で高品質配当株スクリーニング | <span class="badge badge-api">FMP必須</span> <span class="badge badge-optional">FINVIZ任意</span> |
| [VCP Screener]({{ '/ja/skills/vcp-screener/' | relative_url }}) ★ | Minerviniのボラティリティ収縮パターン検出 | <span class="badge badge-api">FMP必須</span> |

★ = 使用例・トラブルシューティング・CLIリファレンスを含む詳細ガイド

全スキルの一覧は[スキルカタログ]({{ '/ja/skill-catalog/' | relative_url }})を参照してください。
