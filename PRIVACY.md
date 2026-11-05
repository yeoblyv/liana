# Liana privacy policy

Last updated: 5 November 2026.

Liana is an add-in for Autodesk Fusion published by Yehor Oblyvantsov,
Groningen, the Netherlands. Contact: support@oblyvantsov.net.

The same text is in Liana itself: open the Liana dialog and expand
Privacy policy.

## 1. What data Liana collects and how it is used

Liana does not collect personal data. It contains no analytics, tracking or
advertising, makes no network connections, and sends nothing to the
publisher or to anyone else.

To work, Liana stores three things on your own computer and in your own
designs:

- Last dialog settings. Written when you click Generate, to the file
  last_settings.json in your user data folder. They hold only the numbers
  and switches of the dialog and are used to open the dialog with your last
  values.
- Build log. Written after every build, to the file build_log.txt in the
  same folder. It is used for troubleshooting and lists the features that
  were skipped and, if a part failed, the error message. Error messages can
  contain folder names on your computer, such as your user name in a path.
  The log stays on your computer unless you choose to send it to someone.
- System settings in the design. When Liana builds a system, the dialog
  values are saved inside that Fusion design, so that running Liana again
  can edit the system. They travel with the design wherever you save or
  share it; how Autodesk stores designs is covered by Autodesk's own terms
  and privacy statement.

The user data folder is %APPDATA%\Liana on Windows and
~/Library/Application Support/Liana on macOS.

## 2. Third parties

Liana shares no data with any third party: no analytics tools, advertising
networks, third-party SDKs, or companies related to the publisher. It
contains no third-party code.

If this ever changes, this policy will be updated before the change is
released, and any third party that receives data will be required to
protect it at least as well as this policy does.

## 3. Retention and deletion

The publisher holds no data from Liana, so there is nothing to retain or
delete on the publisher's side.

On your computer, each Generate replaces the previous settings file and
each build replaces the previous log. Both files stay until you delete
them; uninstalling Liana does not remove them. The values saved in a design
stay part of that design until you delete it.

## 4. Revoking consent and deleting your data

All data stays under your control:

- To stop Liana from storing anything, stop using it and uninstall it.
- To delete the stored files, delete the folder Liana in your user data
  folder (see section 1). Liana works normally afterwards and starts from
  its default settings.
- To delete the values saved in a design, delete the design.

If you write to support@oblyvantsov.net, your message and address are used
only to answer you. They are deleted on request; write to the same address
to ask for that. Issues opened on GitHub are public and are covered by
GitHub's privacy statement.

## Online version

This policy is published at
https://github.com/yeoblyv/liana/blob/main/PRIVACY.md. The Open online
version button under Privacy policy in the Liana dialog opens that page in
your web browser; GitHub's privacy statement applies to that visit.

## Changes

A new version of this policy appears at the address above with a new date,
and in the next release of Liana.
