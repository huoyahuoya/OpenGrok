/*
 * CDDL HEADER START
 *
 * The contents of this file are subject to the terms of the
 * Common Development and Distribution License (the "License").
 * You may not use this file except in compliance with the License.
 *
 * See LICENSE.txt included in this distribution for the specific
 * language governing permissions and limitations under the License.
 *
 * When distributing Covered Code, include this CDDL HEADER in each
 * file and include the License file at LICENSE.txt.
 * If applicable, add the following below this CDDL HEADER, with the
 * fields enclosed by brackets "[]" replaced with your own identifying
 * information: Portions Copyright [yyyy] [name of copyright owner]
 *
 * CDDL HEADER END
 */

/*
 * Copyright (c) 2016, 2019, Oracle and/or its affiliates. All rights reserved.
 */
package opengrok.auth.plugin.ldap;

import java.util.Map;
import java.util.Set;
import opengrok.auth.plugin.entity.User;

public abstract class AbstractLdapProvider {

    /**
     * Lookups user's records
     *
     * @param user find LDAP information about this user
     * @return set of attributes for the user or null
     *
     * @see #lookupLdapContent(opengrok.auth.plugin.entity.User,
     * java.lang.String)
     */
    public Map<String, Set<String>> lookupLdapContent(User user) throws LdapException {
        return lookupLdapContent(user, (String) null);
    }

    /**
     * Lookups user's records
     *
     * @param user find LDAP information about this user
     * @param filter the LDAP filter
     * @return set of attributes for the user or null
     *
     * @see #lookupLdapContent(opengrok.auth.plugin.entity.User,
     * java.lang.String, java.lang.String[])
     */
    public Map<String, Set<String>> lookupLdapContent(User user, String filter) throws LdapException {
        return lookupLdapContent(user, filter, null);
    }

    /**
     * Lookups user's records
     *
     * @param user find LDAP information about this user
     * @param values match these LDAP value
     * @return set of attributes for the user or null
     *
     * @see #lookupLdapContent(opengrok.auth.plugin.entity.User,
     * java.lang.String, java.lang.String[])
     */
    public Map<String, Set<String>> lookupLdapContent(User user, String[] values) throws LdapException {
        return lookupLdapContent(user, null, values);
    }

    /**
     * Lookups user's records
     *
     * @param user find LDAP information about this user
     * @param filter the LDAP filter
     * @param values match these LDAP value
     * @return set of attributes for the user or null
     */
    public abstract Map<String, Set<String>> lookupLdapContent(User user, String filter, String[] values) throws LdapException;

    /**
     * @return if the provider is correctly configured
     */
    public abstract boolean isConfigured();

    /**
     * Closes the LDAP provider.
     */
    public abstract void close();
}
