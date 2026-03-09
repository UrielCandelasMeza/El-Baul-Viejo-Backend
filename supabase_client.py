"""Supabase Client"""
from supabase import create_client, Client
from config import Config

url = Config.SUPABASE_URL
key = Config.SUPABASE_KEY

supabase: Client = create_client(url, key)
