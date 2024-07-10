import time
from .views import (
    website_general_settings,
    website_homepage_settings,
    local_seo_content,
    website_api_keys,
    website_theme_settings,
    website_video,
    website_social_media,
    size_guide,
    website_tracking_script,
    website_city_content,
    website_state_content,
    website_language_settings,
    website_redirects,
    website_testimonials,
    general_pages,
    storage_tip_category,
    blog_category,
    management_pages,
    company_pages,
    storage_types,
    blogs,
    local_blogs,
    blog_author,
    storage_tips,
    featured_page,
    featured_blog,
    facility_token,
    facility_website_settings,
    facility_storagefront_settings,
    facility_coop_settings,
    facility_ti_settings,
    facility_tm_settings,
    facility,
    facility_phone,
    facility_contents,
    facility_merchandise,
    facility_hours,
    facility_geolocation,
    facility_documents,
    facility_business_center_documents,
    facility_insurance,
    facility_promo_review,
    facility_social_media,
    facility_noke_config,
    facility_media,
    owner_media,
    facility_email_notes,
    facility_vehicle_type,
    platform,
    facility_tracking_script,
    rental_fields,
    future_facility,
    well_known,
    render,
    facility_pandadoc_sections,
    landing_page,
    legal_pages,
    owner_facilities,
    facility_blog,
    choices,
    website_amenities,
    website_twilio_settings,
    owner_file_uploads,
    digital_signage,
    facility_unit_info,
    facility_coupon,
    facility_additional_information,
    facility_faq,
    facility_theme,
    website_color_settings,
    owner_pandadoc_credentials,
    military_university_contents,
    facility_update,
    facility_list,
    blacklist,
    website,
    facility_transfer,
    owner_signup,
    kiosk,
    export_reports,
    size_category,
    facility_reviews,
    facility_dni_number,
)

from starlette.responses import JSONResponse
from newrelic.agent import ignore_transaction as nrIgnoreTransactions

facility_prefix = "/v1/owners/{ownerId}/website/facilities/{facilityId}/"
website_prefix = "/v1/owners/{ownerId}/website/"
owner_prefix = "/v1/owners/{ownerId}/"
common_owner_prefix = "/v1/owners/"
platform_owner_prefix = "/v1/platform/owners/{ownerId}/"
platform_facility_prefix = platform_owner_prefix + "facilities/{facilityId}/"
facility_common_prefix = "/v1/owners/{ownerId}/facilities/{facilityId}/"


async def timestamp(request):
    nrIgnoreTransactions(flag=True)
    return JSONResponse({"timestamp": time.time()})


url_patterns = [
    ("/v1/event-handler/render-facility/", render.RendererEventHandler),
    (
        "/v1/event-handler/render-facility-contents/",
        render.RenderFacilityContentEventHandler,
    ),
    ("/v1/event-handler/render-facility-faq/", render.RenderFacilityFAQEventHandler),
    (
        website_prefix + "website-general-settings/",
        website_general_settings.WebsiteGeneralSettingsEndpoint,
    ),
    (common_owner_prefix, owner_facilities.OwnerEndpoint),
    (common_owner_prefix + "export/", export_reports.ExportMarketProCount),
    (website_prefix + "facilities/", facility.FacilityEndpoint),
    (website_prefix + "signup/", owner_signup.ListOwnerSignupEndpoint),
    (
        website_prefix + "website-homepage-settings/",
        website_homepage_settings.WebsiteHomepageSettingsEndpoint,
    ),
    (
        website_prefix + "local-seo-content/",
        local_seo_content.LocalSeoContent,
    ),
    (website_prefix + "website-api-keys/", website_api_keys.WebsiteApiKeysEndpoint),
    (
        website_prefix + "website-theme/",
        website_theme_settings.WebsiteThemeSettingsEndpoint,
    ),
    (website_prefix + "website-video/", website_video.WebsiteVideoEndpoint),
    (
        website_prefix + "website-social-media/",
        website_social_media.WebsiteSocialMediaEndpoint,
    ),
    (
        website_prefix + "website-social-media/{websitesocialmediaId}/",
        website_social_media.DeleteWebsiteSocialMediaEndpoint,
    ),
    (website_prefix + "size-guide/", size_guide.SizeGuideEndpoint),
    (
        website_prefix + "website-tracking-script/",
        website_tracking_script.WebsiteTrackingScriptEndpoint,
    ),
    (
        website_prefix + "website-tracking-script/{trackingscriptId}/",
        website_tracking_script.DeleteWebsiteTrackingScriptEndpoint,
    ),
    (
        website_prefix + "states/{stateSlug}/cities/{citySlug}/",
        website_city_content.WebsiteCityContentEndpoint,
    ),
    (
        website_prefix + "states/{stateSlug}/",
        website_state_content.WebsiteStateContentEndpoint,
    ),
    (
        website_prefix + "website-language-settings/",
        website_language_settings.WebsiteLanguageSettingsEndpoint,
    ),
    (website_prefix + "website-redirects/", website_redirects.WebsiteRedirectsEndpoint),
    (
        website_prefix + "website-redirects/{websiteredirectId}/",
        website_redirects.DeleteWebsiteRedirectsEndpoint,
    ),
    (
        website_prefix + "website-testimonials/",
        website_testimonials.WebsiteTestimonialsEndpoint,
    ),
    (
        website_prefix + "website-testimonials/{testimonialId}/",
        website_testimonials.WebsiteTestimonialsDeletendpoint,
    ),
    (
        website_prefix + "pages/featured-company-pages/",
        featured_page.FeaturedpagesEndpoint,
    ),
    (
        website_prefix + "pages/featured-company-pages/{featuredpageId}/",
        featured_page.DeleteFeaturedpagesEndpoint,
    ),
    (
        website_prefix + "blogs/featured-company-blogs/",
        featured_blog.FeaturedBlogsEndpoint,
    ),
    (
        website_prefix + "blogs/featured-company-blogs/{featuredblogId}/",
        featured_blog.DeleteFeaturedBlogsEndpoint,
    ),
    (website_prefix + "pages/landing-pages/", landing_page.LandingPageEndpoint),
    (
        website_prefix + "pages/landing-pages/{landingpageId}/",
        landing_page.DeleteLandingPageEndpoint,
    ),
    (website_prefix + "pages/general-pages/", general_pages.GeneralPageEndpoint),
    (
        website_prefix + "pages/general-pages/{page_slug}/",
        general_pages.GeneralPageDetailsEndpoint,
    ),
    (
        website_prefix + "tips/{tip_type}/categories/",
        storage_tip_category.TipCategoriesEndpoint,
    ),
    (
        website_prefix + "tips/{tip_type}/categories/{tip_category_slug}/",
        storage_tip_category.TipCategoriesEndpoint,
    ),
    (
        website_prefix + "blogs/{blog_type}/categories/",
        blog_category.BlogCategoriesEndpoint,
    ),
    (
        website_prefix + "blogs/{blog_type}/categories/{slug}/",
        blog_category.BlogCategoryEndpoint,
    ),
    (
        website_prefix + "pages/management-pages/",
        management_pages.ManagementPageEndpoint,
    ),
    (
        website_prefix + "pages/management-pages/{page_slug}/",
        management_pages.ManagementPageDetailsEndpoint,
    ),
    (website_prefix + "pages/company-pages/", company_pages.CompanyPagesEndpoint),
    (
        website_prefix + "pages/company-pages/{page_slug}/",
        company_pages.CompanyPageDetailEndpoint,
    ),
    (website_prefix + "pages/storage-types/", storage_types.StorageTypeEndpoint),
    (
        website_prefix + "pages/storage-types/{page_slug}/",
        storage_types.StorageTypeDetailEndpoint,
    ),
    (website_prefix + "blogs/authors/", blog_author.BlogAuthorsEndpoint),
    (
        website_prefix + "blogs/authors/{author_id}/",
        blog_author.BlogAuthorsEndpoint,
    ),
    (website_prefix + "blogs/{blog_type}/", blogs.BlogsEndpoint),
    (website_prefix + "blogs/{blog_type}/{slug}/", blogs.BlogDetailsEndpoint),
    (website_prefix + "tips/{tips_type}/", storage_tips.TipsEndpoint),
    (
        website_prefix + "tips/{tips_type}/{tip_slug}/",
        storage_tips.TipDetailsEndpoint,
    ),
    (
        facility_prefix + "facility-website-settings/",
        facility_website_settings.FacilityWebsiteSettingsEndpoint,
    ),
    (
        facility_prefix + "facility-storagefront-settings/",
        facility_storagefront_settings.FacilityStorageFrontSettingsEndpoint,
    ),
    (
        facility_prefix + "facility-co-op-settings/",
        facility_coop_settings.FacilityCoOpSettingsEndpoint,
    ),
    (
        facility_prefix + "facility-ti-settings/",
        facility_ti_settings.FacilityTISettingsEndpoint,
    ),
    (
        facility_prefix + "facility-tm-settings/",
        facility_tm_settings.FacilityTMSettingsEndpoint,
    ),
    (facility_prefix, facility.FacilityEndpoint),
    (facility_prefix + "layout/", facility.FacilityLayout),
    (facility_prefix + "phones/", facility_phone.FacilityPhonesEndpoint),
    (
        facility_prefix + "phones/{facilityPhoneId}/",
        facility_phone.DeleteFacilityPhonesEndpoint,
    ),
    (facility_prefix + "facility-contents/", facility_contents.FacilityContentEndpoint),
    (
        facility_prefix + "facility-merchandise-categories/",
        facility_merchandise.FacilityMerchandiseCategoryEndpoint,
    ),
    (
        facility_prefix
        + "facility-merchandise-categories/{facilitymerchandisecategoryId}/",
        facility_merchandise.DeleteFacilityMerchandiseCategoryEndpoint,
    ),
    (facility_prefix + "facility-hours/", facility_hours.FacilityHoursEndpoint),
    (
        facility_prefix + "facility-hours/{facilityhourId}/",
        facility_hours.DeleteFacilityHourEndpoint,
    ),
    (
        facility_prefix + "facility-geolocations/",
        facility_geolocation.FacilityGeoLocationsEndpoint,
    ),
    (
        facility_prefix + "facility-geolocations/{facilitygeolocationId}/",
        facility_geolocation.DeleteFacilityGeoLocationsEndpoint,
    ),
    (facility_prefix + "documents/", facility_documents.FacilityDocumentsEndpoint),
    (
        facility_prefix + "documents/{facilityDocumentId}/",
        facility_documents.DeleteFacilityDocumentEndpoint,
    ),
    (
        facility_prefix + "business-center-documents/",
        facility_business_center_documents.FacilityBusinessCenterDocumentsEndpoint,
    ),
    (
        facility_prefix + "business-center-documents/{businesscenterdocumentId}/",
        facility_business_center_documents.DeleteFacilityBusinessCenterDocumentEndpoint,
    ),
    (
        facility_prefix + "facility-insurances/",
        facility_insurance.FacilityInsuranceEndpoint,
    ),
    (facility_prefix + "promo/", facility_promo_review.FacilityPromosEndpoint),
    (
        facility_prefix + "facility-reviews/",
        facility_promo_review.FacilityUserReviewsEndpoint,
    ),
    (
        facility_prefix + "facility-social-media/",
        facility_social_media.FacilitySocialMediaEndpoint,
    ),
    (
        facility_prefix + "facility-social-media/{facilitysocialmediaId}/",
        facility_social_media.DeleteFacilitySocialMediaEndpoint,
    ),
    (
        facility_prefix + "facility-noke-configuration/",
        facility_noke_config.FacilityNokeConfigurationEndpoint,
    ),
    (facility_prefix + "facility-media/", facility_media.FacilityMediaEndpoint),
    (
        facility_prefix + "facility-media/{facilitymediaId}/",
        facility_media.DeleteFacilityMediaEndpoint,
    ),
    (website_prefix + "default-media/", owner_media.OwnerMediaEndpoint),
    (
        website_prefix + "default-media/{defaultmediaId}/",
        owner_media.DeleteOwnerMediaEndpoint,
    ),
    (
        facility_prefix + "pandadoc/sections/",
        facility_pandadoc_sections.PandadocSectionsEndpoint,
    ),
    # facility email note end point
    (facility_prefix + "email-notes/", facility_email_notes.FacilityEmailNotesEndpoint),
    (
        facility_prefix + "email-notes/{emailnoteid}/",
        facility_email_notes.DeleteFacilityEmailNotesEndpoint,
    ),
    (
        facility_prefix + "newsletter-subscribers/",
        facility_promo_review.FacilityNewsLetterSubscribersEndpoint,
    ),
    (
        facility_prefix + "vehicle-types/",
        facility_vehicle_type.FacilityVehicleTypeEndpoint,
    ),
    (
        facility_prefix + "vehicle-types/{facilityVehicleTypeId}/",
        facility_vehicle_type.DeleteFacilityVehicleTypeEndpoint,
    ),
    (
        facility_prefix + "facility-merchandises/",
        facility_merchandise.FacilityMerchandiseEndpoint,
    ),
    (
        facility_prefix + "facility-merchandises/{facilitymerchandiseId}/",
        facility_merchandise.DeleteFacilityMerchandiseEndpoint,
    ),
    (facility_prefix + "rental-fields/", rental_fields.RentalFieldsEndpoint),
    # Platform related api endpoints
    ("/.well-known/gds/", well_known.applicationConfig),
    (owner_prefix + "applications/", platform.ApplicationsEndpoint),
    (owner_prefix + "extensions/", platform.OwnerExtensionsEndpoint),
    (
        owner_prefix + "facilities/{facilityId}/extensions/",
        platform.FacilityExtensionsEndpoint,
    ),
    # facility tracking script endpoints
    (
        facility_prefix + "tracking-script/",
        facility_tracking_script.FacilityTrackingScriptEndpoint,
    ),
    (
        facility_prefix + "tracking-script/{trackingscriptId}/",
        facility_tracking_script.DeleteFacilityTrackingScriptEndpoint,
    ),
    (platform_owner_prefix, platform.PlatformAppMainPage),
    (platform_owner_prefix + "website/theme/", platform.PlatformAppThemePage),
    (platform_owner_prefix + "website/", platform.PlatformAppCMSPage),
    (platform_facility_prefix + "manage_units/", platform.PlatformAppFacilityPage),
    # Future facility
    (facility_prefix + "future/", future_facility.FutureFacilityEndpoint),
    (facility_prefix + "render/", render.FacilityRenderEndpoint),
    (
        facility_prefix + "facility-contents/render/",
        render.FacilityContentRenderEndpoint,
    ),
    (website_prefix + "pages/legal-pages/", legal_pages.LegalPageEndpoint),
    (
        website_prefix + "pages/legal-pages/{page_slug}/",
        legal_pages.LegalPageDetailsEndpoint,
    ),
    (website_prefix + "cities/", website_city_content.WebsiteCityListEndpoint),
    (website_prefix + "states/", website_state_content.WebsiteStateListEndpoint),
    (owner_prefix + "facilities/", owner_facilities.OwnerFacilitiesEndpoint),
    (owner_prefix + "facilities/export/", export_reports.ExportOwnerFacilities),
    (facility_prefix + "blogs/", facility_blog.FacilityBlogEndpoint),
    (facility_prefix + "blogs/{blogid}/", facility_blog.DeleteFacilityBlogEndpoint),
    (website_prefix + "choices/{choiceclasstype}/", choices.ChoicesTypesEndpoint),
    (website_prefix + "amenities/", website_amenities.WebsiteAmenitiesEndpoint),
    ("/v1/amenities/default-amenities/", website_amenities.DefaultAmenitiesEndpoint),
    (
        "/v1/amenities/default-amenities/{amenityId}/",
        website_amenities.DeleteDefaultAmenitiesEndpoint,
    ),
    (
        website_prefix + "amenities/owner-amenities/",
        website_amenities.OwnerAmenitiesEndpoint,
    ),
    (
        website_prefix + "amenities/owner-amenities/{amenityId}/",
        website_amenities.DeleteOwnerAmenitiesEndpoint,
    ),
    (website_prefix + "twilio-conf/", website_twilio_settings.WebsiteTwilioEndpoint),
    (owner_prefix + "files/", owner_file_uploads.OwnerFileUploadEndpoint),
    (owner_prefix + "download-token/", facility_token.DownloadPDFEndpoint),
    (
        owner_prefix + "files/{fileId}/",
        owner_file_uploads.DeleteOwnerFileUploadEndpoint,
    ),
    (
        facility_prefix + "digital-signage/presentations/",
        digital_signage.DigitalSignageEndpoint,
    ),
    (
        owner_prefix + "digital-signage/presentations/",
        digital_signage.ListAllPresentationsEndpoint,
    ),
    (
        facility_prefix + "digital-signage/presentations/{presentationId}/",
        digital_signage.FacilityPresentationEndpoint,
    ),
    (
        owner_prefix + "digital-signage/presentations/{presentationId}/",
        digital_signage.PresentationEndpoint,
    ),
    (facility_prefix + "space-types/", facility_unit_info.SpaceTypeInfoEndpoint),
    (facility_prefix + "facility-coupon/", facility_coupon.FacilityCouponEndpoint),
    (
        facility_prefix + "facility-coupon/{couponId}/",
        facility_coupon.DeleteFacilityCouponEndpoint,
    ),
    (
        facility_common_prefix + "additional-information/",
        facility_additional_information.FacilityAdditionInfoEndpoint,
    ),
    (
        owner_prefix + "facilities/additional-information/",
        facility_additional_information.FacilityAdditionInfoEndpoint,
    ),
    (facility_prefix + "local-blog/", local_blogs.LocalBlogsEndpoint),
    (facility_prefix + "faq/", facility_faq.FacilityFaqEndpoint),
    (facility_prefix + "facility-theme/", facility_theme.FacilityThemeEndpoint),
    (
        website_prefix + "website-colors/",
        website_color_settings.WebsiteColorSettingsEndpoint,
    ),
    (
        "/v1/facilities/additional-information/",
        facility_additional_information.FacilityAdditionInfoEndpoint,
    ),
    (
        website_prefix + "pandadoc_credentials/",
        owner_pandadoc_credentials.OwnerPandadocCredentials,
    ),
    (facility_prefix + "refresh/", facility_update.FacilityUpdate),
    (
        facility_prefix + "documents/{facilityDocumentId}/token/",
        facility_documents.FacilityDocumentTokenEndpoint,
    ),
    (
        "/v1/contents/military/",
        military_university_contents.MilitaryContentsEndpoint,
    ),
    (
        "/v1/contents/universities/",
        military_university_contents.UniversityContentsEndpoint,
    ),
    (
        "/v1/contents/military/{militaryContentSlug}/",
        military_university_contents.ManageMilitaryContentsEndpoint,
    ),
    (
        "/v1/contents/universities/{universityContentSlug}/",
        military_university_contents.ManageUniversityContentsEndpoint,
    ),
    (owner_prefix, owner_facilities.OwnerInformationsEndpoint),
    ("/v1/facilities/", facility_list.ListFacility),
    ("/v1/blacklist/", blacklist.BlackList),
    ("/v1/blacklist/{id}/", blacklist.BlackList),
    ("/v1/websites/", website.AllWebsiteEndpoint),
    (owner_prefix + "websites/", website.WebsitesEndpoint),
    (
        owner_prefix + "transfers/",
        facility_transfer.FacilityTransferEndpoint,
    ),
    (
        owner_prefix + "transfers/{transferId}/",
        facility_transfer.FacilityTransferEndpoint,
    ),
    (owner_prefix + "kiosk/configuration/", kiosk.KioskConfigEndpoint),
    (facility_prefix + "size-categories/", size_category.FacilitySizeCategory),
    (owner_prefix + "size-categories/", size_category.OwnerSizeCategory),
    (
        owner_prefix + "digital-signage/presentations/{presentationId}/assign/",
        digital_signage.AssignPresentationsEndpoint,
    ),
    (
        owner_prefix + "digital-signage/presentations/{presentationId}/duplicate/",
        digital_signage.DuplicatePresentationsEndpoint,
    ),
    (website_prefix + "signup/{signupId}/", owner_signup.OwnerSignupEndpoint),
    (
        facility_prefix + "space-types/{spaceTypeId}/",
        facility_unit_info.DeleteSpaceTypeInfoEndpoint,
    ),
    (owner_prefix + "platform/extensions/", platform.PlatformExtensionsEndpoint),
    (facility_prefix + "reviews/", facility_reviews.FacilityReviewEndpoint),
    (facility_prefix + "numbers/", facility_dni_number.FacilityDniNumberEndpoint),
    (
        facility_prefix + "numbers/{dniNumberId}/",
        facility_dni_number.DeleteFacilityDniNumberEndpoint,
    ),
    (facility_prefix + "reviews_data/", facility_reviews.FacilityReviewDateEndpoint)
]
