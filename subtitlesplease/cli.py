# -*- coding: utf-8 -*-

import click
import subtitlesplease

@click.command()
def main(args=None):
    subp = subtitlesplease.SubtitlesPlease()
    subp.run()


if __name__ == "__main__":
    main()
