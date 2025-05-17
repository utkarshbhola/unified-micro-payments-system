// test-supabase.ts
import { supabase } from './supabase-client';

async function testSupabase() {
    const { data, error } = await supabase.from('users').select('*');
    console.log('Users:', data);

  if (error) console.error('Error:', error);
}

testSupabase();