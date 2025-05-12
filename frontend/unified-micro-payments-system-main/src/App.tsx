import React from 'react';
import SendMoney from './components/sendMoney';
import ReceiveQR from './components/receiverQR';
import TransactionHistory from './components/TransactionalHistory';
import UserDashboard from './components/UserDashboard';

const App: React.FC = () => {
  return (
    <div className="bg-gray-100 min-h-screen p-6">
      <UserDashboard />
      <SendMoney />
      <ReceiveQR />
      <TransactionHistory />
    </div>
  );
};

export default App;
