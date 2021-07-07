import React, { useContext } from 'react';
import {
  BrowserRouter as Router,
  Redirect,
  Route,
  Switch
} from 'react-router-dom'

import LoginPanel from './components/LoginPanel'
import UserPanel from './layouts/userPanel'
import { AuthContext } from './context/AuthContext';
import './App.css'


function App() {
  const { tokenPayload } = useContext(AuthContext)

  return (
    <div className="App">
      <Router>
        {!tokenPayload ? <Redirect to="/login" /> : null}
        <Switch>
          <Route
            component={LoginPanel}
            path='/login'
          />
          <Route
            component={UserPanel}
            path='/'
          />
        </Switch>
      </Router>
    </div>
  );
}

export default App;
