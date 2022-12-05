import React, { Component } from 'react';

class Navbar extends Component {
    render() {
        return (
            <nav className='Header py-2 mb-4' style={{ backgroundColor: "#f0f5f5" }}>
                <div className='container text-center'>
                    <div className="d-flex align-items-center justify-content-center">
                        <div href='/' class='navbar-brand'>La Música</div>
                    </div>

                </div>
            </nav>
        );
    }
} export default Navbar;