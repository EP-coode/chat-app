import React from 'react';
import {
  BrowserRouter as Router,
  Route,
  Switch
} from 'react-router-dom'

import LoginPanel from './components/LoginPanel'
import UserPanel from './layouts/UserPanel'
import './App.css'


function App() {

  return (
    <div className="App">
      <Router>
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
