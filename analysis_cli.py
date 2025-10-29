import click
from tabulate import tabulate
from analysis_db import AnalysisDB

@click.group()
def cli():
    """CLI для просмотра результатов анализа."""
    pass

@cli.command()
@click.option('--limit', default=5, help='Количество последних результатов')
def latest(limit):
    """Показать последние результаты анализа."""
    db = AnalysisDB()
    results = db.get_latest_analyses(limit)
    _print_results(results)

@cli.command()
@click.argument('signal_type')
def by_signal(signal_type):
    """Поиск по типу сигнала (BUY/SELL/HOLD)."""
    db = AnalysisDB()
    results = db.search_by_signal(signal_type.upper())
    _print_results(results)

@cli.command()
@click.argument('asset')
def by_asset(asset):
    """Поиск по активу (например: BTC, ETH)."""
    db = AnalysisDB()
    results = db.search_by_asset(asset.upper())
    _print_results(results)

def _print_results(results):
    """Форматирует и выводит результаты в виде таблицы."""
    if not results:
        click.echo("Результатов не найдено")
        return

    # Подготовка данных для таблицы
    headers = ["ID", "Signal", "Asset", "Conf", "Risk", "Price Target", "Summary"]
    rows = []
    for r in results:
        price_info = r["price_targets"]
        price_str = f"Entry: {price_info.get('entry', '-')}, Target: {price_info.get('target', '-')}"
        
        rows.append([
            r["message_id"],
            r["signal_type"],
            ", ".join(r["assets_mentioned"]),
            r["confidence_level"],
            r["risk_level"],
            price_str,
            r["summary"][:50] + "..." if len(r["summary"]) > 50 else r["summary"]
        ])

    click.echo(tabulate(rows, headers=headers, tablefmt="grid"))
    click.echo(f"\nВсего найдено: {len(results)}")

if __name__ == "__main__":
    cli()