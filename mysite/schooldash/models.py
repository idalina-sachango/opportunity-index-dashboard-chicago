from curses import def_prog_mode
from django.db import models
import sqlite3
import pandas as pd

class cps(models.Model):
    h = models.CharField(max_length=200, default="CPS")

    def __str__(self):
        return f"{self.header}"
