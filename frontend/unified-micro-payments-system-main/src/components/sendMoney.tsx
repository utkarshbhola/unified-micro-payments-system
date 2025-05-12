import React from 'react';

const SendMoney: React.FC = () => {
  return (
    <div className="p-4 border rounded-xl shadow-md w-full max-w-md mx-auto mt-6">
      <h2 className="text-xl font-bold mb-4">Send Money</h2>
      <input className="border p-2 w-full mb-2" placeholder="Recipient UPI ID" />
      <input className="border p-2 w-full mb-2" placeholder="Amount" type="number" />
      <button className="bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 w-full">
        Send
      </button>
    </div>
  );
};

export default SendMoney;
