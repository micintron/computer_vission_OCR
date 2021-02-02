import React from 'react';
import './Sidebar.scss';
import logo from '../../images/USCISlogo.png';
import passport from '../../images/passport.png';
import pdf from '../../images/pdf-file.png';
import imageIcon from '../../images/image-icon.png';
import licenseIcon from '../../images/driver-license.png';
import sentimentIcon from '../../images/feeling.png';
import avatarIcon from '../../images/avatar.jpeg';
import { NavLink } from 'react-router-dom'

class Sidebar extends React.Component {

    constructor(props) {

        super(props);

        this.state = {

        }
    }
 
    render() {
        
        return (

            <div className="sidebar-container"> 
                
                <img src={logo} className="logo" alt="Logo" width="50" />

                <div className="navigation-container">

                    <NavLink className="navigation-item-container" to="/ocr/passport" activeClassName="selected" isActive={() => window.location.pathname === '/ocr/passport'}>
                        <div className="navigation-item">
                            <img src={passport} className="icon" alt="Icon" width="21" />
                            Passport
                        </div>
                    </NavLink>

                    <NavLink className="navigation-item-container" to="/ocr/pdf" activeClassName="selected" isActive={() => window.location.pathname === '/ocr/pdf'}>
                        <div className="navigation-item">
                            <img src={pdf} className="icon" alt="Icon" width="21" />
                            Pdf
                        </div>
                    </NavLink>

                    <NavLink className="navigation-item-container" to="/ocr/image" activeClassName="selected" isActive={() => window.location.pathname === '/ocr/image'}>
                        <div className="navigation-item">
                            <img src={imageIcon} className="icon" alt="Icon" width="21" />
                            Image
                        </div>
                    </NavLink>

                    <NavLink className="navigation-item-container" to="/ocr/license" activeClassName="selected" isActive={() => window.location.pathname === '/ocr/license'}>
                        <div className="navigation-item">
                            <img src={licenseIcon} className="icon" alt="Icon" width="21" />
                            Drivers License
                        </div>
                    </NavLink>

                    <NavLink className="navigation-item-container" to="/analysis/text" activeClassName="selected" isActive={() => window.location.pathname === '/analysis/text'}>
                        <div className="navigation-item">
                            <img src={sentimentIcon} className="icon" alt="Icon" width="21" />
                            Text Analysis
                        </div>
                    </NavLink>
                </div>

                <div className="profile-container">
                    <img src={avatarIcon} className="avatar" alt="Avatar" width="50" />
                    <span>John Doe</span>
                </div>
            </div>
            
        );
    }

}

export default Sidebar;