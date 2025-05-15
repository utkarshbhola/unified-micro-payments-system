import React, { useState } from 'react';

const SendMoney: React.FC = () => {
  const [senderUPI, setSenderUPI] = useState('');
  const [receiverUPI, setReceiverUPI] = useState('');
  const [amount, setAmount] = useState<number>(0);
  const [message, setMessage] = useState('');

  const handleSend = async () => {
    try{
      const res = await fetch('http://localhost:8000/send', {
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

      if (res.ok) {
        setMessage('✅ Money sent successfully!');
      } else {
        setMessage(`❌ Error: ${JSON.stringify(data.detail)}`);
      }
    } catch (error) {
      console.error('Error:', error);
      setMessage('❌ Error: Unable to send money. Please try again.');
      return;

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


