# Make sure you have installed the 'supabase' Python package:
# pip install supabase

from supabase import create_client, Client

SUPABASE_URL = 'https://txuoicvalrtadkrxmqvr.supabase.co'
SUPABASE_KEY ='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4dW9pY3ZhbHJ0YWRrcnhtcXZyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc0MjE4NDAsImV4cCI6MjA2Mjk5Nzg0MH0.hrLDn10sJCIXXAQ3Hs5U66UbX0RmIlQPDPdXFgyrvZM'


supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
