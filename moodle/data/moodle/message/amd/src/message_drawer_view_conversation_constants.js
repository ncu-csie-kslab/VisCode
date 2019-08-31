// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Moodle is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Moodle.  If not, see <http://www.gnu.org/licenses/>.

/**
 * Constant values for the conversation page in the message drawer.
 *
 * @module     core_message/message_drawer_view_conversation_constants
 * @copyright  2018 Ryan Wyllie <ryan@moodle.com>
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */
define([], function() {

    var SELECTORS = {
        ACTION_ACCEPT_CONTACT_REQUEST: '[data-action="accept-contact-request"]',
        ACTION_CANCEL_CONFIRM: '[data-action="cancel-confirm"]',
        ACTION_CANCEL_EDIT_MODE: '[data-action="cancel-edit-mode"]',
        ACTION_CONFIRM_ADD_CONTACT: '[data-action="confirm-add-contact"]',
        ACTION_CONFIRM_BLOCK: '[data-action="confirm-block"]',
        ACTION_CONFIRM_DELETE_SELECTED_MESSAGES: '[data-action="confirm-delete-selected-messages"]',
        ACTION_CONFIRM_DELETE_CONVERSATION: '[data-action="confirm-delete-conversation"]',
        ACTION_CONFIRM_FAVOURITE: '[data-action="confirm-favourite"]',
        ACTION_CONFIRM_MUTE: '[data-action="confirm-mute"]',
        ACTION_CONFIRM_UNFAVOURITE: '[data-action="confirm-unfavourite"]',
        ACTION_CONFIRM_REMOVE_CONTACT: '[data-action="confirm-remove-contact"]',
        ACTION_CONFIRM_UNBLOCK: '[data-action="confirm-unblock"]',
        ACTION_CONFIRM_UNMUTE: '[data-action="confirm-unmute"]',
        ACTION_DECLINE_CONTACT_REQUEST: '[data-action="decline-contact-request"]',
        ACTION_REQUEST_ADD_CONTACT: '[data-action="request-add-contact"]',
        ACTION_REQUEST_BLOCK: '[data-action="request-block"]',
        ACTION_REQUEST_DELETE_CONVERSATION: '[data-action="request-delete-conversation"]',
        ACTION_REQUEST_DELETE_SELECTED_MESSAGES: '[data-action="delete-selected-messages"]',
        ACTION_REQUEST_REMOVE_CONTACT: '[data-action="request-remove-contact"]',
        ACTION_REQUEST_UNBLOCK: '[data-action="request-unblock"]',
        ACTION_VIEW_CONTACT: '[data-action="view-contact"]',
        ACTION_VIEW_GROUP_INFO: '[data-action="view-group-info"]',
        CAN_RECEIVE_FOCUS: 'input:not([type="hidden"]), a[href], button, textarea, select, [tabindex]',
        CONFIRM_DIALOGUE_BUTTON_TEXT: '[data-region="dialogue-button-text"]',
        CONFIRM_DIALOGUE_CANCEL_BUTTON: '[data-action="cancel-confirm"]',
        CONFIRM_DIALOGUE_CONTAINER: '[data-region="confirm-dialogue-container"]',
        CONFIRM_DIALOGUE_HEADER: '[data-region="dialogue-header"]',
        CONFIRM_DIALOGUE_TEXT: '[data-region="dialogue-text"]',
        CONTACT_REQUEST_SENT_MESSAGE_CONTAINER: '[data-region="contact-request-sent-message-container"]',
        CONTENT_PLACEHOLDER_CONTAINER: '[data-region="content-placeholder"]',
        CONTENT_CONTAINER: '[data-region="content-container"]',
        CONTENT_MESSAGES_CONTAINER: '[data-region="content-message-container"]',
        CONTENT_MESSAGES_FOOTER_CONTAINER: '[data-region="content-messages-footer-container"]',
        CONTENT_MESSAGES_FOOTER_EDIT_MODE_CONTAINER: '[data-region="content-messages-footer-edit-mode-container"]',
        CONTENT_MESSAGES_FOOTER_REQUIRE_CONTACT_CONTAINER: '[data-region="content-messages-footer-require-contact-container"]',
        CONTENT_MESSAGES_FOOTER_REQUIRE_UNBLOCK_CONTAINER: '[data-region="content-messages-footer-require-unblock-container"]',
        CONTENT_MESSAGES_FOOTER_UNABLE_TO_MESSAGE_CONTAINER: '[data-region="content-messages-footer-unable-to-message"]',
        DAY_MESSAGES_CONTAINER: '[data-region="day-messages-container"]',
        DELETE_MESSAGES_FOR_ALL_USERS_TOGGLE: '[data-region="delete-messages-for-all-users-toggle"]',
        DELETE_MESSAGES_FOR_ALL_USERS_TOGGLE_CONTAINER: '[data-region="delete-messages-for-all-users-toggle-container"]',
        FAVOURITE_ICON_CONTAINER: '[data-region="favourite-icon-container"]',
        FOOTER_CONTAINER: '[data-region="content-messages-footer-container"]',
        HEADER: '[data-region="header-content"]',
        HEADER_EDIT_MODE: '[data-region="header-edit-mode"]',
        HEADER_PLACEHOLDER_CONTAINER: '[data-region="header-placeholder"]',
        LOADING_ICON_CONTAINER: '[data-region="loading-icon-container"]',
        MESSAGE: '[data-region="message"]',
        MESSAGE_NOT_SELECTED: '[data-region="message"][aria-checked="false"]',
        MESSAGE_NOT_SELECTED_ICON: '[data-region="not-selected-icon"]',
        MESSAGE_SELECTED_ICON: '[data-region="selected-icon"]',
        MESSAGES: '[data-region="content-message-container"]',
        MESSAGES_CONTAINER: '[data-region="content-message-container"]',
        MESSAGES_SELECTED_COUNT: '[data-region="message-selected-court"]',
        MESSAGE_TEXT_AREA: '[data-region="send-message-txt"]',
        MORE_MESSAGES_LOADING_ICON_CONTAINER: '[data-region="more-messages-loading-icon-container"]',
        MUTED_ICON_CONTAINER: '[data-region="muted-icon-container"]',
        PLACEHOLDER_CONTAINER: '[data-region="placeholder-container"]',
        SELF_CONVERSATION_MESSAGE_CONTAINER: '[data-region="self-conversation-message-container"]',
        SEND_MESSAGE_BUTTON: '[data-action="send-message"]',
        SEND_MESSAGE_ICON_CONTAINER: '[data-region="send-icon-container"]',
        TEXT: '[data-region="text"]',
        TITLE: '[data-region="title"]'
    };

    var TEMPLATES = {
        HEADER_PRIVATE: 'core_message/message_drawer_view_conversation_header_content_type_private',
        HEADER_PRIVATE_NO_CONTROLS: 'core_message/message_drawer_view_conversation_header_content_type_private_no_controls',
        HEADER_PUBLIC: 'core_message/message_drawer_view_conversation_header_content_type_public',
        HEADER_SELF: 'core_message/message_drawer_view_conversation_header_content_type_self',
        DAY: 'core_message/message_drawer_view_conversation_body_day',
        MESSAGE: 'core_message/message_drawer_view_conversation_body_message',
        MESSAGES: 'core_message/message_drawer_view_conversation_body_messages'
    };

    // Conversation types. They must have the same values defined in \core_message\api.
    var CONVERSATION_TYPES = {
        PRIVATE: 1,
        PUBLIC: 2,
        SELF: 3
    };

    return {
        SELECTORS: SELECTORS,
        TEMPLATES: TEMPLATES,
        CONVERSATION_TYPES: CONVERSATION_TYPES,
        NEWEST_MESSAGES_FIRST: true,
        LOAD_MESSAGE_LIMIT: 100,
        MILLISECONDS_IN_SEC: 1000
    };
});
