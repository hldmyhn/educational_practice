from logging import INFO, basicConfig


def setup_logging() -> None:
    basicConfig(
        level=INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )


__all__ = ["setup_logging",]
