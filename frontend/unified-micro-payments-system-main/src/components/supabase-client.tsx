
import { createClient } from '@supabase/supabase-js'

const supabaseUrl = 'https://txuoicvalrtadkrxmqvr.supabase.co'
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR4dW9pY3ZhbHJ0YWRrcnhtcXZyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDc0MjE4NDAsImV4cCI6MjA2Mjk5Nzg0MH0.hrLDn10sJCIXXAQ3Hs5U66UbX0RmIlQPDPdXFgyrvZM'
export const supabase = createClient(supabaseUrl, supabaseKey)