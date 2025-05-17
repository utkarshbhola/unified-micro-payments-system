import React, { useState } from 'react';
import { supabase } from './supabase-client'; // adjust the path as needed

const SendMoney: React.FC = () => {
  const [senderUPI, setSenderUPI] = useState('');
  const [receiverUPI, setReceiverUPI] = useState('');
  const [amount, setAmount] = useState<number>(0);
  const [message, setMessage] = useState('');

  const handleSend = async () => {
    try {
      // Basic input validation
      if (!senderUPI || !receiverUPI || amount <= 0) {
        setMessage('❌ Please fill all fields with valid data.');
        return;
      }

      if (senderUPI === receiverUPI) {
        setMessage('❌ Sender and receiver cannot be the same.');
        return;
      }

      // ✅ Check if both users exist
      const { data: sender, error: senderError } = await supabase
        .from('users')
        .select('upi_id, balance')
        .eq('upi_id', senderUPI)
        .single();

      const { data: receiver, error: receiverError } = await supabase
        .from('users')
        .select('upi_id')
        .eq('upi_id', receiverUPI)
        .single();

      if (senderError || !sender) {
        setMessage('❌ Sender UPI not found.');
        return;
      }

      if (receiverError || !receiver) {
        setMessage('❌ Receiver UPI not found.');
        return;
      }

      if (sender.balance < amount) {
        setMessage('❌ Insufficient balance.');
        return;
      }

      // 🧾 Call your backend to handle money transfer
      const res = await fetch('http://localhost:8800/send', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          payer_id: senderUPI,
          payee_id: receiverUPI,
          amount: amount,
        }),
      });

      const data = await res.json();
      console.log('Response:', data);

      if (!res.ok) {
        setMessage(`❌ Error: ${JSON.stringify(data.detail)}`);
        return;
      }

      // 💾 Log transaction in Supabase
      const { error: insertError } = await supabase.from('transactions').insert([
        {
          payer_id: senderUPI,
          payee_id: receiverUPI,
          amount: amount,
          timestamp: new Date().toISOString(),
        },
      ]);

      if (insertError) {
        console.error('Supabase error:', insertError);
        setMessage(`⚠️ Money sent but failed to log transaction: ${insertError.message}`);
        return;
      }

      // ✅ Success message
      setMessage('✅ Money sent and recorded successfully!');
    } catch (error) {
      console.error('Unexpected Error:', error);
      setMessage('❌ Error: Unable to send money. Please try again.');
    }
  };

  return (
    <div className="p-4 border rounded-xl shadow-md w-full max-w-md mx-auto mt-6">
      <h2 className="text-xl font-bold mb-4">Send Money</h2>
      <input
        className="border p-2 w-full mb-2"
        placeholder="Your UPI ID"
        value={senderUPI}
        onChange={(e) => setSenderUPI(e.target.value)}
      />
      <input
        className="border p-2 w-full mb-2"
        placeholder="Receiver UPI ID"
        value={receiverUPI}
        onChange={(e) => setReceiverUPI(e.target.value)}
      />
      <input
        type="number"
        className="border p-2 w-full mb-2"
        placeholder="Amount"
        value={amount}
        onChange={(e) => setAmount(Number(e.target.value))}
      />
      <button
        onClick={handleSend}
        className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 w-full"
      >
        Send
      </button>
      {message && <p className="mt-4 text-center">{message}</p>}
    </div>
  );
};

export default SendMoney;
